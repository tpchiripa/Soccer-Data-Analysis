from src.services.player_service import PlayerService
from src.services.profile_service import PlayerProfileService

# ---------------------------------------------------------
# Shared Player Service
# ---------------------------------------------------------

player_service = PlayerService(
    "data/raw/database.sqlite"
)

# ---------------------------------------------------------
# Profile Service
# ---------------------------------------------------------

service = PlayerProfileService(
    player_service
)

service.summary()

print()

profile = service.get_profile("Lionel Messi")

print("=" * 60)
print("PLAYER PROFILE")
print("=" * 60)
print(profile)