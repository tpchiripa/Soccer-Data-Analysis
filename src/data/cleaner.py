"""
cleaner.py

Responsible for cleaning raw football datasets before feature engineering.
"""

from __future__ import annotations

import pandas as pd


class SoccerDataCleaner:
    """Clean and prepare football datasets."""

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Default cleaning method.

        Currently assumes the dataframe is Player_Attributes.
        This becomes the standard interface used by the pipeline.
        """
        return self.clean_player_attributes(df)

    def clean_player_attributes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the Player_Attributes table.
        """

        df = df.copy()

        # Remove duplicate records
        df = df.drop_duplicates()

        # Convert date column
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # Remove rows without player id
        if "player_api_id" in df.columns:
            df = df.dropna(subset=["player_api_id"])

        # Fill numeric columns using median
        numeric_cols = df.select_dtypes(include="number").columns

        for column in numeric_cols:
            df[column] = df[column].fillna(df[column].median())

        # Fill categorical columns using mode
        categorical_cols = df.select_dtypes(include="object").columns

        for column in categorical_cols:
            if not df[column].mode().empty:
                df[column] = df[column].fillna(df[column].mode()[0])

        return df

    def clean_players(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean Player table.
        """

        df = df.copy()

        df = df.drop_duplicates()

        return df