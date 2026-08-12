"""
watchlist_service.py
Manages a shared watchlist of players scouts and federations are tracking
for potential call-ups or transfer targets.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

import pandas as pd

from src.services.player_service import PlayerService


class WatchlistService:
    """
    Add, remove, and list players on the shared watchlist.
    """

    def __init__(self, player_service: PlayerService, db_path: str):
        self.player_service = player_service
        self.db_path = db_path
        self._ensure_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _ensure_table(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS Watchlist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_api_id INTEGER NOT NULL UNIQUE,
                    note TEXT,
                    added_at TEXT NOT NULL
                )
                """
            )

    # ---------------------------------------------------------
    # Add Player
    # ---------------------------------------------------------
    def add(self, player_api_id: int, note: str = "") -> dict:
        player = self.player_service.get(player_api_id)
        if player is None:
            raise ValueError(f"Player with id {player_api_id} not found.")

        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO Watchlist (player_api_id, note, added_at)
                VALUES (?, ?, ?)
                """,
                (player_api_id, note, datetime.now(timezone.utc).isoformat()),
            )

        return {"player_api_id": player_api_id, "status": "added"}

    # ---------------------------------------------------------
    # Remove Player
    # ---------------------------------------------------------
    def remove(self, player_api_id: int) -> dict:
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM Watchlist WHERE player_api_id = ?",
                (player_api_id,),
            )
        return {"player_api_id": player_api_id, "status": "removed"}

    # ---------------------------------------------------------
    # List Watchlist
    # ---------------------------------------------------------
    def list(self) -> pd.DataFrame:
        with self._connect() as conn:
            watchlist = pd.read_sql(
                """
                SELECT player_api_id, note, added_at
                FROM Watchlist
                ORDER BY added_at DESC
                """,
                conn,
            )

        if watchlist.empty:
            return watchlist

        players = self.player_service.dataset()
        merged = watchlist.merge(players, on="player_api_id", how="left")

        return merged[
            [
                "player_api_id",
                "player_name",
                "overall_rating",
                "potential",
                "note",
                "added_at",
            ]
        ]