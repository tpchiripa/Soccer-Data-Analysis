from src.services.similarity_service import SimilarityService

service = SimilarityService("data/raw/database.sqlite")

service.summary()

print()

print("=" * 60)
print("PLAYERS SIMILAR TO LIONEL MESSI")
print("=" * 60)

print(service.recommend("Lionel Messi"))

print()

print("=" * 60)
print("PLAYERS SIMILAR TO CRISTIANO RONALDO")
print("=" * 60)

print(service.recommend("Cristiano Ronaldo"))

print()

print("=" * 60)
print("PLAYERS SIMILAR TO NEYMAR")
print("=" * 60)

print(service.recommend("Neymar"))