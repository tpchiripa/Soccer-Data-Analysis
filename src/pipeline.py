"""
pipeline.py

Orchestrates the complete FootballIQ data pipeline.
"""

from src.data.loader import SoccerDataLoader
from src.data.cleaner import SoccerDataCleaner
from src.data.features import FeatureEngineer
from src.data.validator import DataValidator


class FootballPipeline:
    """
    Runs the complete data pipeline.

    Steps
    -----
    1. Load data
    2. Validate data
    3. Clean data
    4. Engineer features
    """

    def __init__(self, db_path: str):

        self.loader = SoccerDataLoader(db_path)
        self.cleaner = SoccerDataCleaner()
        self.engineer = FeatureEngineer()

    def run(self):

        print("=" * 60)
        print("FOOTBALLIQ PIPELINE")
        print("=" * 60)

        # -------------------------
        # Load
        # -------------------------

        print("\nLoading Player Attributes...")

        df = self.loader.load_player_attributes()

        print(f"Loaded {len(df):,} rows")

        # -------------------------
        # Validate
        # -------------------------

        print("\nRunning Data Validation...")

        validator = DataValidator(df)

        report = validator.generate_report()

        print("Validation Complete")

        # -------------------------
        # Clean
        # -------------------------

        print("\nCleaning Dataset...")

        cleaned_df = self.cleaner.clean(df)

        print(f"Rows after cleaning: {len(cleaned_df):,}")

        # -------------------------
        # Feature Engineering
        # -------------------------

        print("\nEngineering Features...")

        X = self.engineer.prepare_features(cleaned_df)

        print(f"Feature Matrix Shape: {X.shape}")

        print("\nPipeline Finished Successfully.")

        return report, cleaned_df, X