"""
similarity_service.py

High-level service for finding similar football players.
"""

from __future__ import annotations

import pandas as pd

from src.models.similarity import PlayerSimilarity
from src.services.player_service import PlayerService


class SimilarityService:
    """
    Business service for player similarity.
    """

    def __init__(self, player_service: PlayerService):

        print("Initializing Similarity Service...")

        self.player_service = player_service

        # Shared player dataset
        self.players = self.player_service.dataset()

        # Shared feature matrix
        self.X = self.player_service.features()

        # Train similarity model
        self.model = PlayerSimilarity(n_neighbors=6)

        self.model.fit(
            self.X,
            self.players
        )

        print("Similarity model ready.")

    # ---------------------------------------------------------
    # Find Similar Players
    # ---------------------------------------------------------

    def similar_players(
        self,
        player_name: str,
        top_n: int = 5
    ) -> pd.DataFrame:
        """
        Find players with similar attributes.
        """

        results = self.model.find_similar(player_name)

        # Remove queried player
        results = results[
            results["player_name"].str.lower()
            != player_name.lower()
        ]

        return (
            results[
                [
                    "player_api_id",
                    "player_name",
                    "overall_rating",
                    "potential",
                    "distance",
                ]
            ]
            .sort_values("distance")
            .head(top_n)
            .reset_index(drop=True)
        )

    # ---------------------------------------------------------
    # Player Exists
    # ---------------------------------------------------------

    def player_exists(self, player_name: str) -> bool:
        """
        Check whether a player exists.
        """

        return not self.player_service.search(player_name).empty

    # ---------------------------------------------------------
    # Recommend Similar Players
    # ---------------------------------------------------------

    def recommend(
        self,
        player_name: str,
        top_n: int = 5
    ) -> pd.DataFrame:
        """
        Recommend similar players.
        """

        if not self.player_exists(player_name):
            raise ValueError(
                f"Player '{player_name}' was not found."
            )

        return self.similar_players(
            player_name,
            top_n
        )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self):

        print("=" * 60)
        print("SIMILARITY SERVICE")
        print("=" * 60)
        print(f"Players Loaded : {self.player_service.count():,}")
        print(f"Features       : {self.X.shape[1]}")
        print(f"Observations   : {self.X.shape[0]:,}")
        print("=" * 60)