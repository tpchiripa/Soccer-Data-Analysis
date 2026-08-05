from src.data.loader import SoccerDataLoader
from src.data.validator import DataValidator

loader = SoccerDataLoader("data/raw/database.sqlite")

df = loader.load_table("Player_Attributes")

validator = DataValidator(df)

report = validator.generate_report()

print("=" * 60)
print("DATA QUALITY REPORT")
print("=" * 60)

print(f"\nRows: {report['rows']}")
print(f"Columns: {report['columns']}")
print(f"Duplicate Rows: {report['duplicates']}")

print("\nColumns with Missing Values")
print("----------------------------")
print(report["missing_values"])

print("\nNon Numeric Columns")
print("-------------------")
print(report["non_numeric_columns"])

print("\nInvalid Rating Columns")
print("----------------------")
print(report["invalid_ratings"])