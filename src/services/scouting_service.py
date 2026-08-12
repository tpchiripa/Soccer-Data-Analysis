"""
scouting_service.py

Provides scouting and player discovery services for FootballIQ.
"""

from __future__ import annotations

import pandas as pd

from src.services.player_service import PlayerService


class ScoutingService:
    """
    Search and filter players using scouting criteria.
    """

    def __init__(self, player_service: PlayerService):

        self.player_service = player_service

        # Shared player dataset
        self.players = self.player_service.dataset()

    # ---------------------------------------------------------
    # Scout Players
    # ---------------------------------------------------------

    def scout(
        self,
        min_overall: float | None = None,
        min_potential: float | None = None,
        preferred_foot: str | None = None,
        min_height: float | None = None,
        max_height: float | None = None,
        min_weight: float | None = None,
        max_weight: float | None = None,
        limit: int = 20,
    ) -> pd.DataFrame:
        """
        Filter players using common scouting criteria.
        """

        df = self.players.copy()

        if min_overall is not None:
            df = df[df["overall_rating"] >= min_overall]

        if min_potential is not None:
            df = df[df["potential"] >= min_potential]

        if preferred_foot is not None:
            df = df[
                df["preferred_foot"].str.lower()
                == preferred_foot.lower()
            ]

        if min_height is not None:
            df = df[df["height"] >= min_height]

        if max_height is not None:
            df = df[df["height"] <= max_height]

        if min_weight is not None:
            df = df[df["weight"] >= min_weight]

        if max_weight is not None:
            df = df[df["weight"] <= max_weight]

        return (
            df[
                [
                    "player_api_id",
                    "player_name",
                    "overall_rating",
                    "potential",
                    "preferred_foot",
                    "height",
                    "weight",
                ]
            ]
            .sort_values(
                ["overall_rating", "potential"],
                ascending=False,
            )
            .head(limit)
            .reset_index(drop=True)
        )

    # ---------------------------------------------------------
    # Search by Attribute
    # ---------------------------------------------------------

    def by_attribute(
        self,
        attribute: str,
        minimum: float,
        limit: int = 20,
    ) -> pd.DataFrame:
        """
        Search players by a football attribute.
        """

        if attribute not in self.players.columns:
            raise ValueError(
                f"'{attribute}' is not a valid attribute."
            )

        df = self.players[
            self.players[attribute] >= minimum
        ]

        return (
            df[
                [
                    "player_name",
                    attribute,
                    "overall_rating",
                    "potential",
                ]
            ]
            .sort_values(
                attribute,
                ascending=False,
            )
            .head(limit)
            .reset_index(drop=True)
        )

    # ---------------------------------------------------------
    # Elite Prospects
    # ---------------------------------------------------------

    def elite_prospects(
        self,
        potential: float = 90,
        overall: float = 75,
        limit: int = 20,
    ) -> pd.DataFrame:
        """
        Find elite young prospects.
        """

        df = self.players[
            (self.players["potential"] >= potential)
            &
            (self.players["overall_rating"] >= overall)
        ]

        return (
            df[
                [
                    "player_name",
                    "overall_rating",
                    "potential",
                ]
            ]
            .sort_values(
                ["potential", "overall_rating"],
                ascending=False,
            )
            .head(limit)
            .reset_index(drop=True)
        )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self):

        print("=" * 60)
        print("SCOUTING SERVICE")
        print("=" * 60)
        print(
            f"Players Loaded : {self.player_service.count():,}"
        )
        print("=" * 60)