from src.pipeline import FootballPipeline
from src.models.clustering import PlayerClusterModel
from src.models.cluster_analysis import ClusterAnalyzer
from src.data.features import FeatureEngineer


def main():

    print("=" * 60)
    print("FOOTBALLIQ MODEL TRAINING")
    print("=" * 60)

    # Run data pipeline
    pipeline = FootballPipeline("data/raw/database.sqlite")

    report, df, X = pipeline.run()

    # Train clustering model
    model = PlayerClusterModel(n_clusters=6)

    labels = model.train(X)

    # Analyse clusters
    analyzer = ClusterAnalyzer(df, labels)

    analyzer.print_report(
        FeatureEngineer.FEATURE_COLUMNS
    )

    # Training summary
    print("\nTraining Complete")
    print("-" * 30)

    print(f"Number of clusters : {len(set(labels))}")
    print(f"Players clustered  : {len(labels):,}")

    model.summary()

    # Save trained model
    model.save()

    print("\nTraining finished successfully.")


if __name__ == "__main__":
    main()