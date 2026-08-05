from src.pipeline import FootballPipeline

pipeline = FootballPipeline("data/raw/database.sqlite")

report, df, X = pipeline.run()

print("\nValidation Summary")
print("------------------")

print(f"Rows: {report['rows']}")
print(f"Columns: {report['columns']}")
print(f"Duplicates: {report['duplicates']}")

print("\nPipeline Output")
print("------------------")

print(df.head())

print("\nFeature Matrix")

print(X.shape)