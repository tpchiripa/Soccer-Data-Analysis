"""
loader.py

Handles loading data from the European Soccer SQLite database.
"""

from pathlib import Path
import sqlite3
import pandas as pd


class SoccerDataLoader:
    """Loads tables from the European Soccer Database."""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)

        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Database not found: {self.db_path}"
            )

    def connect(self):
        """Create SQLite connection."""
        return sqlite3.connect(self.db_path)

    def load_table(self, table_name: str) -> pd.DataFrame:
        """Load any table into a pandas DataFrame."""
        with self.connect() as conn:
            query = f"SELECT * FROM {table_name}"
            return pd.read_sql(query, conn)

    def available_tables(self):
        """Return list of database tables."""
        with self.connect() as conn:
            query = """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name;
            """
            return pd.read_sql(query, conn)