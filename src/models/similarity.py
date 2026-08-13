"""
similarity.py

Machine learning model for finding similar football players.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


class PlayerSimilarity:
    """
    Nearest Neighbors model for player similarity.
    """

    def __init__(self, n_neighbors: int = 6):

        self.n_neighbors = n_neighbors

        self.model = NearestNeighbors(
            n_neighbors=n_neighbors,
            metric="euclidean"
        )

        self.players = None
        self.features = None

    # ---------------------------------------------------------
    # Train Model
    # ---------------------------------------------------------

    def fit(self, X, players):
        """
        Train the similarity model.

        Parameters
        ----------
        X : pandas.DataFrame or numpy.ndarray
            Feature matrix.

        players : pandas.DataFrame
            Player dataframe.
        """

        self.features = X
        self.players = players.reset_index(drop=True)

        self.model.fit(X)

    # ---------------------------------------------------------
    # Find Similar Players
    # ---------------------------------------------------------

    def find_similar(self, player_name: str) -> pd.DataFrame:
        """
        Find players similar to the given player.

        Parameters
        ----------
        player_name : str
            Name of the player.

        Returns
        -------
        pandas.DataFrame
            Similar players ordered by distance.
        """

        # Locate player
        matches = self.players[
            self.players["player_name"].str.lower() == player_name.lower()
        ]

        if matches.empty:
            raise ValueError(
                f"Player '{player_name}' not found."
            )

        # Row index of player
        index = matches.index[0]

        # -----------------------------------------------------
        # Prepare feature vector
        # -----------------------------------------------------

        if isinstance(self.features, pd.DataFrame):

            # Keep as DataFrame so feature names are preserved
            player_vector = self.features.iloc[[index]]

        elif isinstance(self.features, np.ndarray):

            player_vector = self.features[index].reshape(1, -1)

        else:
            raise TypeError(
                "Feature matrix must be a pandas DataFrame or NumPy array."
            )

        # -----------------------------------------------------
        # Find nearest neighbours
        # -----------------------------------------------------

        distances, indices = self.model.kneighbors(player_vector)

        # -----------------------------------------------------
        # Build result dataframe
        # -----------------------------------------------------

        results = self.players.iloc[indices[0]].copy()

        results["distance"] = distances[0]

        results = results.sort_values(
            by="distance",
            ascending=True
        ).reset_index(drop=True)

        return results