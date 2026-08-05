"""
Feature engineering module.

Responsible for selecting, validating and scaling football player
attributes for machine learning models.
"""

from __future__ import annotations

from typing import List, Tuple

import pandas as pd
from sklearn.preprocessing import StandardScaler


class FeatureEngineer:
    """
    Handles feature engineering for machine learning.
    """

    # Core football attributes
    DEFAULT_FEATURES = [

        # Attacking
        "crossing",
        "finishing",
        "heading_accuracy",
        "volleys",
        "short_passing",
        "long_passing",
        "shot_power",
        "long_shots",
        "positioning",

        # Technical
        "dribbling",
        "curve",
        "free_kick_accuracy",
        "ball_control",

        # Defensive
        "marking",
        "standing_tackle",
        "sliding_tackle",
        "interceptions",

        # Physical
        "strength",
        "stamina",
        "aggression",
        "balance",
        "reactions",
        "jumping",

        # Goalkeeping
        "gk_diving",
        "gk_handling",
        "gk_kicking",
        "gk_positioning",
        "gk_reflexes",

        # Overall
        "overall_rating",
        "potential"
    ]

    def __init__(self):

        self.scaler = StandardScaler()

    def available_features(
        self,
        df: pd.DataFrame
    ) -> List[str]:
        """
        Return features that exist in the dataframe.
        """

        return [
            feature
            for feature in self.DEFAULT_FEATURES
            if feature in df.columns
        ]

    def prepare_features(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Select only ML features.
        """

        features = self.available_features(df)

        return df[features].copy()

    def scale_features(
        self,
        X: pd.DataFrame
    ) -> Tuple[pd.DataFrame, StandardScaler]:
        """
        Scale numerical features.
        """

        scaled = self.scaler.fit_transform(X)

        X_scaled = pd.DataFrame(
            scaled,
            columns=X.columns,
            index=X.index
        )

        return X_scaled, self.scaler

    def transform(
        self,
        X: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Transform new data using fitted scaler.
        """

        scaled = self.scaler.transform(X)

        return pd.DataFrame(
            scaled,
            columns=X.columns,
            index=X.index
        )