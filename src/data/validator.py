"""
validator.py

Performs data quality validation on the Player_Attributes dataset.
"""

import pandas as pd


class DataValidator:
    """Validates a football dataset before it enters the ML pipeline."""

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def check_empty(self):
        """Ensure the dataframe is not empty."""
        if self.df.empty:
            raise ValueError("Dataset is empty.")

    def check_required_columns(self, required_columns):
        """Ensure all required columns exist."""
        missing = [col for col in required_columns if col not in self.df.columns]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

    def check_missing_values(self):
        """Return columns containing missing values."""
        missing = self.df.isnull().sum()
        missing = missing[missing > 0]

        return missing.sort_values(ascending=False)

    def check_duplicates(self):
        """Return duplicate row count."""
        return self.df.duplicated().sum()

    def check_numeric_columns(self):
        """Return columns that are not numeric."""
        non_numeric = []

        for column in self.df.columns:
            if not pd.api.types.is_numeric_dtype(self.df[column]):
                non_numeric.append(column)

        return non_numeric

    def check_rating_ranges(self):
        """
        Football ratings should be between 0 and 100.
        """

        rating_columns = [
            column
            for column in self.df.columns
            if column not in [
                "id",
                "player_fifa_api_id",
                "player_api_id"
            ]
        ]

        invalid = {}

        for column in rating_columns:

            if pd.api.types.is_numeric_dtype(self.df[column]):

                outside_range = self.df[
                    (self.df[column] < 0) |
                    (self.df[column] > 100)
                ]

                if len(outside_range) > 0:
                    invalid[column] = len(outside_range)

        return invalid

    def generate_report(self):
        """Generate a complete validation report."""

        self.check_empty()

        report = {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "duplicates": self.check_duplicates(),
            "missing_values": self.check_missing_values(),
            "non_numeric_columns": self.check_numeric_columns(),
            "invalid_ratings": self.check_rating_ranges()
        }

        return report