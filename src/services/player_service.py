"""
player_service.py

Provides player search, lookup and feature access services
for FootballIQ.
"""

from __future__ import annotations

import pandas as pd

from src.data.loader import SoccerDataLoader
from src.data.cleaner import SoccerDataCleaner
from src.data.features import FeatureEngineer


class PlayerService:
    """
    Service responsible for player retrieval,
    searching and feature preparation.
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

        # Keep only the latest record for each player
        self.attributes = (
            self.attributes
            .sort_values("date")
            .groupby("player_api_id")
            .tail(1)
        )

        # Merge player names with latest attributes
        self.players = self.players.merge(
            self.attributes,
            on="player_api_id",
            how="inner"
        )

        print(f"Loaded {len(self.players):,} players.")

    # ---------------------------------------------------------
    # Search Players
    # ---------------------------------------------------------

    def search(self, name: str) -> pd.DataFrame:

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
                    "potential"
                ]
            ]
            .sort_values(
                "overall_rating",
                ascending=False
            )
            .reset_index(drop=True)
        )

    # ---------------------------------------------------------
    # Get Player by API ID
    # ---------------------------------------------------------

    def get_player(self, player_api_id: int):

        player = self.players[
            self.players["player_api_id"] == player_api_id
        ]

        if player.empty:
            return None

        return player.iloc[0]

    # ---------------------------------------------------------
    # Get Player Profile
    # ---------------------------------------------------------

    def player_profile(self, player_api_id: int):

        player = self.get_player(player_api_id)

        if player is None:
            return None

        return {
            "player_api_id": int(player["player_api_id"]),
            "player_name": player["player_name"],
            "overall_rating": float(player["overall_rating"]),
            "potential": float(player["potential"]),
            "preferred_foot": player.get("preferred_foot"),
            "height": player.get("height"),
            "weight": player.get("weight"),
            "birthday": player.get("birthday"),
        }

    # ---------------------------------------------------------
    # Top Rated Players
    # ---------------------------------------------------------

    def top_players(self, n: int = 20):

        return (
            self.players[
                [
                    "player_name",
                    "overall_rating",
                    "potential"
                ]
            ]
            .sort_values(
                "overall_rating",
                ascending=False
            )
            .head(n)
            .reset_index(drop=True)
        )

    # ---------------------------------------------------------
    # Number of Players
    # ---------------------------------------------------------

    def count(self):

        return len(self.players)

    # ---------------------------------------------------------
    # Return Full Dataset
    # ---------------------------------------------------------

    def get_players(self):

        """
        Returns the merged player dataframe.
        """

        return self.players.copy()

    # ---------------------------------------------------------
    # Return Feature Matrix
    # ---------------------------------------------------------

    def get_feature_matrix(self):

        """
        Returns the scaled machine learning feature matrix.
        """

        return self.engineer.prepare_features(
            self.players
        )