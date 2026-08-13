"""
cluster_analysis.py

Utilities for analysing KMeans player clusters.
"""

import pandas as pd


class ClusterAnalyzer:
    """
    Analyse player clusters and generate summaries.
    """

    def __init__(self, dataframe: pd.DataFrame, labels):
        self.df = dataframe.copy()
        self.df["cluster"] = labels

    def cluster_sizes(self):
        """
        Number of players in each cluster.
        """
        return self.df["cluster"].value_counts().sort_index()

    def cluster_summary(self):
        """
        Return summary statistics for each cluster.
        """

        summary = (
            self.df.groupby("cluster")
            .agg(
                players=("cluster", "count"),
                avg_rating=("overall_rating", "mean"),
                avg_potential=("potential", "mean")
            )
            .round(2)
        )

        return summary

    def top_attributes(self, feature_columns, top_n=5):
        """
        Return the strongest average attributes
        for every cluster.
        """

        results = {}

        grouped = self.df.groupby("cluster")

        for cluster_id, cluster_df in grouped:

            averages = cluster_df[feature_columns].mean()

            top = averages.sort_values(
                ascending=False
            ).head(top_n)

            results[cluster_id] = top

        return results

    def print_report(self, feature_columns):

        print("=" * 60)
        print("CLUSTER REPORT")
        print("=" * 60)

        print("\nCluster Summary")
        print("----------------")

        print(self.cluster_summary())

        print("\nTop Attributes")
        print("----------------")

        attributes = self.top_attributes(feature_columns)

        for cluster, values in attributes.items():

            print(f"\nCluster {cluster}")

            for feature, score in values.items():
                print(f"  {feature:<25}{score:.2f}")