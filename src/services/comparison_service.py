"""
comparison_service.py

Provides player-to-player comparison services for FootballIQ.
"""

from __future__ import annotations

import pandas as pd

from src.services.profile_service import PlayerProfileService


class ComparisonService:
    """
    Compares two football players.
    """

    def __init__(self, profile_service: PlayerProfileService):

        self.profile_service = profile_service

    # ---------------------------------------------------------
    # Compare Players
    # ---------------------------------------------------------

    def compare(
        self,
        player_one: str,
        player_two: str
    ) -> pd.DataFrame:
        """
        Compare two players side-by-side.
        """

        p1 = self.profile_service.get_profile(player_one)
        p2 = self.profile_service.get_profile(player_two)

        return pd.DataFrame(
            {
                "Attribute": [
                    "Overall Rating",
                    "Potential",
                    "Preferred Foot",
                    "Height",
                    "Weight",
                ],
                p1["player_name"]: [
                    p1["overall_rating"],
                    p1["potential"],
                    p1["preferred_foot"],
                    p1["height"],
                    p1["weight"],
                ],
                p2["player_name"]: [
                    p2["overall_rating"],
                    p2["potential"],
                    p2["preferred_foot"],
                    p2["height"],
                    p2["weight"],
                ],
            }
        )

    # ---------------------------------------------------------
    # Compare Top Attributes
    # ---------------------------------------------------------

    def compare_top_attributes(
        self,
        player_one: str,
        player_two: str
    ) -> pd.DataFrame:
        """
        Compare the strongest attributes of two players.
        """

        p1 = self.profile_service.get_profile(player_one)
        p2 = self.profile_service.get_profile(player_two)

        top1 = dict(p1["top_attributes"])
        top2 = dict(p2["top_attributes"])

        attributes = sorted(
            set(top1).union(top2)
        )

        rows = []

        for attribute in attributes:

            rows.append(
                {
                    "Attribute": attribute,
                    p1["player_name"]: top1.get(attribute, "-"),
                    p2["player_name"]: top2.get(attribute, "-"),
                }
            )

        return pd.DataFrame(rows)

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self):

        print("=" * 60)
        print("PLAYER COMPARISON SERVICE")
        print("=" * 60)
        print(
            f"Players Loaded : "
            f"{self.profile_service.player_service.count():,}"
        )
        print("=" * 60)