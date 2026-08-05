from src.services.player_service import PlayerService

service = PlayerService("data/raw/database.sqlite")

print()

print("=" * 60)
print("PLAYER SEARCH")
print("=" * 60)

print(service.search("messi"))

print()

print("=" * 60)
print("TOP PLAYERS")
print("=" * 60)

print(service.top_players(10))

print()

print("=" * 60)
print("PLAYER COUNT")
print("=" * 60)

print(service.count())