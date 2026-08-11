from src.services.player_service import PlayerService
from src.services.scouting_service import ScoutingService

player_service = PlayerService(
    "data/raw/database.sqlite"
)

service = ScoutingService(
    player_service
)

service.summary()

print()

print("=" * 60)
print("TOP LEFT-FOOTED PLAYERS")
print("=" * 60)
print(
    service.scout(
        preferred_foot="left",
        min_overall=85
    )
)

print()

print("=" * 60)
print("BEST DRIBBLERS")
print("=" * 60)
print(
    service.by_attribute(
        "dribbling",
        minimum=95
    )
)

print()

print("=" * 60)
print("ELITE PROSPECTS")
print("=" * 60)
print(
    service.elite_prospects()
)