from src.data.loader import SoccerDataLoader
from src.data.cleaner import SoccerDataCleaner
from src.data.features import FeatureEngineer

DATABASE = "data/raw/database.sqlite"

print("=" * 60)
print("FOOTBALLIQ DATA PIPELINE TEST")
print("=" * 60)

loader = SoccerDataLoader(DATABASE)

print("\nLoading Player_Attributes table...")

df = loader.load_table("Player_Attributes")

print(f"Loaded {len(df)} rows")
print(f"Columns: {len(df.columns)}")

cleaner = SoccerDataCleaner()

df = cleaner.clean_player_attributes(df)

print(f"\nRows after cleaning: {len(df)}")

engineer = FeatureEngineer()

X = engineer.prepare_features(df)

print("\nSelected Features")
print("-----------------")
print(X.columns.tolist())

X_scaled, scaler = engineer.scale_features(X)

print("\nScaled Dataset Shape")
print("--------------------")
print(X_scaled.shape)

print("\nPipeline completed successfully!")
