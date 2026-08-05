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

    def __init__(self, db_path: str):

        print("Initializing Similarity Service...")

        self.player_service = PlayerService(db_path)

        self.players = self.player_service.get_players()

        self.X = self.player_service.get_feature_matrix()

        self.model = PlayerSimilarity(n_neighbors=6)

        self.model.fit(self.X, self.players)

        print("Similarity model ready.")

    # ---------------------------------------------------------
    # Find Similar Players
    # ---------------------------------------------------------

    def similar_players(self, player_name: str, top_n: int = 5):

        """
        Find players with similar attributes.

        Parameters
        ----------
        player_name : str
            Player to search.

        top_n : int
            Number of similar players to return.

        Returns
        -------
        pandas.DataFrame
        """

        results = self.model.find_similar(player_name)

        # Remove the queried player
        results = results[
            results["player_name"].str.lower() != player_name.lower()
        ]

        columns = [
            "player_api_id",
            "player_name",
            "overall_rating",
            "potential",
            "distance"
        ]

        return (
            results[columns]
            .sort_values("distance")
            .head(top_n)
            .reset_index(drop=True)
        )

    # ---------------------------------------------------------
    # Player Exists
    # ---------------------------------------------------------

    def player_exists(self, player_name: str) -> bool:

        return not self.player_service.search(player_name).empty

    # ---------------------------------------------------------
    # Search then Recommend
    # ---------------------------------------------------------

    def recommend(self, player_name: str):

        if not self.player_exists(player_name):

            raise ValueError(
                f"Player '{player_name}' was not found."
            )

        return self.similar_players(player_name)

    # ---------------------------------------------------------
    # Service Summary
    # ---------------------------------------------------------

    def summary(self):

        print("=" * 60)
        print("SIMILARITY SERVICE")
        print("=" * 60)

        print(f"Players Loaded : {self.player_service.count():,}")
        print(f"Features       : {self.X.shape[1]}")
        print(f"Observations   : {self.X.shape[0]:,}")