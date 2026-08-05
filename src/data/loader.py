"""
loader.py

Handles loading data from the European Soccer SQLite database.
"""

from pathlib import Path
import sqlite3
import pandas as pd


class SoccerDataLoader:
    """
    Loads data from the European Soccer SQLite database.
    """

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)

        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Database not found: {self.db_path}"
            )

    def connect(self):
        """Create and return a SQLite connection."""
        return sqlite3.connect(self.db_path)

    def load_table(self, table_name: str) -> pd.DataFrame:
        """
        Load any table from the database.

        Parameters
        ----------
        table_name : str
            Name of the SQLite table.

        Returns
        -------
        pandas.DataFrame
        """
        with self.connect() as conn:
            query = f"SELECT * FROM {table_name}"
            return pd.read_sql(query, conn)

    def available_tables(self):
        """
        Return all available tables in the database.
        """
        with self.connect() as conn:
            query = """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name;
            """
            return pd.read_sql(query, conn)

    # ======================================================
    # Convenience Methods
    # ======================================================

    def load_player_attributes(self):
        """Load the Player_Attributes table."""
        return self.load_table("Player_Attributes")

    def load_players(self):
        """Load the Player table."""
        return self.load_table("Player")

    def load_matches(self):
        """Load the Match table."""
        return self.load_table("Match")

    def load_teams(self):
        """Load the Team table."""
        return self.load_table("Team")

    def load_team_attributes(self):
        """Load the Team_Attributes table."""
        return self.load_table("Team_Attributes")

    def load_leagues(self):
        """Load the League table."""
        return self.load_table("League")

    def load_countries(self):
        """Load the Country table."""
        return self.load_table("Country")