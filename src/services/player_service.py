"""
player_service.py

Provides player search, retrieval and feature access services
for FootballIQ.
"""

from __future__ import annotations

import pandas as pd

from src.data.loader import SoccerDataLoader
from src.data.cleaner import SoccerDataCleaner
from src.data.features import FeatureEngineer


class PlayerService:
    """
    Core service responsible for loading, searching and
    retrieving player information throughout FootballIQ.
    """

    def __init__(self, db_path: str):

        self.loader = SoccerDataLoader(db_path)
        self.cleaner = SoccerDataCleaner()
        self.engineer = FeatureEngineer()

        self.players = None
        self.attributes = None

        self.load_data()

    # ---------------------------------------------------------
    # Load Data
    # ---------------------------------------------------------

    def load_data(self):

        print("Loading players...")

        self.players = self.loader.load_players()

        print("Loading player attributes...")

        self.attributes = self.loader.load_player_attributes()

        self.attributes = self.cleaner.clean(
            self.attributes
        )

        # Keep only latest record per player
        self.attributes = (
            self.attributes
            .sort_values("date")
            .groupby("player_api_id")
            .tail(1)
        )

        # Merge player information
        self.players = (
            self.players.merge(
                self.attributes,
                on="player_api_id",
                how="inner"
            )
            .reset_index(drop=True)
        )

        print(f"Loaded {len(self.players):,} players.")

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(self, name: str) -> pd.DataFrame:
        """
        Search players by name.
        """

        matches = self.players[
            self.players["player_name"]
            .str.contains(name, case=False, na=False)
        ]

        return (
            matches[
                [
                    "player_api_id",
                    "player_name",
                    "overall_rating",
                    "potential",
                ]
            ]
            .sort_values(
                "overall_rating",
                ascending=False,
            )
            .reset_index(drop=True)
        )

    # ---------------------------------------------------------
    # Get Player
    # ---------------------------------------------------------

    def get(self, player_api_id: int):
        """
        Retrieve one player by API ID.
        """

        player = self.players[
            self.players["player_api_id"] == player_api_id
        ]

        if player.empty:
            return None

        return player.iloc[0]

    # ---------------------------------------------------------
    # Player Profile
    # ---------------------------------------------------------

    def player_profile(self, player_api_id: int):
        """
        Return a lightweight player profile dictionary.
        """

        player = self.get(player_api_id)

        if player is None:
            return None

        return {
            "player_api_id": int(player["player_api_id"]),
            "player_name": player["player_name"],
            "overall_rating": float(player["overall_rating"]),
            "potential": float(player["potential"]),
            "preferred_foot": player.get("preferred_foot"),
            "height": int(player["height"]),
            "weight": int(player["weight"]),
            "birthday": player.get("birthday"),
        }

    # ---------------------------------------------------------
    # Top Players
    # ---------------------------------------------------------

    def top(self, limit: int = 20) -> pd.DataFrame:
        """
        Return the highest-rated players.
        """

        return (
            self.players[
                [
                    "player_name",
                    "overall_rating",
                    "potential",
                ]
            ]
            .sort_values(
                "overall_rating",
                ascending=False,
            )
            .head(limit)
            .reset_index(drop=True)
        )

    # ---------------------------------------------------------
    # Dataset
    # ---------------------------------------------------------

    def dataset(self) -> pd.DataFrame:
        """
        Return the merged player dataset.
        """

        return self.players.copy()

    # ---------------------------------------------------------
    # Feature Matrix
    # ---------------------------------------------------------

    def features(self):
        """
        Return the machine-learning feature matrix.
        """

        return self.engineer.prepare_features(
            self.players
        )

    # ---------------------------------------------------------
    # Count
    # ---------------------------------------------------------

    def count(self) -> int:
        """
        Number of loaded players.
        """

        return len(self.players)

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self):

        print("=" * 60)
        print("PLAYER SERVICE")
        print("=" * 60)
        print(f"Players Loaded : {self.count():,}")
        print(f"Columns        : {len(self.players.columns)}")
        print("=" * 60)

    # =========================================================
    # Backward Compatibility
    # =========================================================

    def get_player(self, player_api_id: int):
        """
        Alias for get().
        """
        return self.get(player_api_id)

    def top_players(self, n: int = 20):
        """
        Alias for top().
        """
        return self.top(n)

    def get_players(self):
        """
        Alias for dataset().
        """
        return self.dataset()

    def get_feature_matrix(self):
        """
        Alias for features().
        """
        return self.features()