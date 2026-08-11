"""
profile_service.py

Generates rich player profiles for FootballIQ.
"""

from __future__ import annotations

from src.services.player_service import PlayerService


class PlayerProfileService:
    """
    Generates detailed player profiles.
    """

    def __init__(self, player_service: PlayerService):

        self.player_service = player_service

    # ---------------------------------------------------------
    # Player Profile
    # ---------------------------------------------------------

    def get_profile(self, player_name: str) -> dict:
        """
        Return a complete player profile.
        """

        results = self.player_service.search(player_name)

        if results.empty:
            raise ValueError(
                f"Player '{player_name}' not found."
            )

        player_id = results.iloc[0]["player_api_id"]

        player = self.player_service.get_player(player_id)

        if player is None:
            raise ValueError(
                f"Player '{player_name}' not found."
            )

        profile = self.player_service.player_profile(player_id)

        profile["top_attributes"] = self.top_attributes(player)

        return profile

    # ---------------------------------------------------------
    # Top Attributes
    # ---------------------------------------------------------

    def top_attributes(self, player, top_n: int = 5):

        ignore = {
            "id",
            "player_api_id",
            "player_fifa_api_id",
            "player_name",
            "birthday",
            "date",
            "overall_rating",
            "potential",
            "preferred_foot",
            "attacking_work_rate",
            "defensive_work_rate",
            "height",
            "weight",
        }

        numeric = {}

        for column in player.index:

            if column in ignore:
                continue

            value = player[column]

            if isinstance(value, (int, float)):
                numeric[column] = float(value)

        return sorted(
            numeric.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:top_n]

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self):

        print("=" * 60)
        print("PLAYER PROFILE SERVICE")
        print("=" * 60)
        print(f"Players Loaded : {self.player_service.count():,}")
        print("=" * 60)