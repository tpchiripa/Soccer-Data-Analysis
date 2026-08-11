from src.services.player_service import PlayerService
from src.services.profile_service import PlayerProfileService
from src.services.comparison_service import ComparisonService

player_service = PlayerService(
    "data/raw/database.sqlite"
)

profile_service = PlayerProfileService(
    player_service
)

service = ComparisonService(
    profile_service
)

service.summary()

print()

print("=" * 60)
print("MESSI vs RONALDO")
print("=" * 60)
print(
    service.compare(
        "Lionel Messi",
        "Cristiano Ronaldo"
    )
)

print()

print("=" * 60)
print("TOP ATTRIBUTES")
print("=" * 60)
print(
    service.compare_top_attributes(
        "Lionel Messi",
        "Cristiano Ronaldo"
    )
)