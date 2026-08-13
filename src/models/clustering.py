"""
clustering.py

Machine Learning clustering module for FootballIQ.

Responsible for:
- Training the KMeans model
- Predicting player clusters
- Saving trained models
- Loading trained models
"""

from pathlib import Path

import joblib
import numpy as np
from sklearn.cluster import KMeans


class PlayerClusterModel:
    """
    KMeans clustering model for football players.
    """

    def __init__(self, n_clusters: int = 6, random_state: int = 42):

        self.n_clusters = n_clusters
        self.random_state = random_state

        self.model = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            n_init=10
        )

    # -------------------------------------------------------
    # Train Model
    # -------------------------------------------------------

    def train(self, X):

        """
        Train the clustering model.

        Parameters
        ----------
        X : numpy.ndarray
            Scaled feature matrix.
        """

        self.model.fit(X)

        return self.model.labels_

    # -------------------------------------------------------
    # Predict
    # -------------------------------------------------------

    def predict(self, X):

        """
        Predict cluster assignments.
        """

        return self.model.predict(X)

    # -------------------------------------------------------
    # Cluster Centers
    # -------------------------------------------------------

    def cluster_centers(self):

        """
        Return cluster centroids.
        """

        return self.model.cluster_centers_

    # -------------------------------------------------------
    # Inertia
    # -------------------------------------------------------

    def inertia(self):

        """
        Return model inertia.
        """

        return self.model.inertia_

    # -------------------------------------------------------
    # Save
    # -------------------------------------------------------

    def save(self, filepath="models/kmeans.pkl"):

        """
        Save trained model.
        """

        path = Path(filepath)

        path.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(self.model, path)

        print(f"Model saved -> {path}")

    # -------------------------------------------------------
    # Load
    # -------------------------------------------------------

    def load(self, filepath="models/kmeans.pkl"):

        """
        Load trained model.
        """

        self.model = joblib.load(filepath)

        print(f"Model loaded <- {filepath}")

        return self.model

    # -------------------------------------------------------
    # Summary
    # -------------------------------------------------------

    def summary(self):

        """
        Display model information.
        """

        print("=" * 60)
        print("PLAYER CLUSTER MODEL")
        print("=" * 60)

        print(f"Clusters : {self.n_clusters}")
        print(f"Inertia  : {self.model.inertia_:,.2f}")