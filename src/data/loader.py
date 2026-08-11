"""
loader.py

Data access layer for the European Soccer SQLite database.
"""

from __future__ import annotations

from pathlib import Path
import sqlite3

import pandas as pd


class SoccerDataLoader:
    """
    Data access layer for the European Soccer Database.

    Responsible only for reading data from SQLite.
    """

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------

    def __init__(self, db_path: str):

        self.db_path = Path(db_path)

        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Database not found: {self.db_path}"
            )

    # ---------------------------------------------------------
    # Database Connection
    # ---------------------------------------------------------

    def connect(self) -> sqlite3.Connection:
        """
        Create a SQLite connection.
        """

        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # Generic Loader
    # ---------------------------------------------------------

    def load_table(self, table_name: str) -> pd.DataFrame:
        """
        Load an entire table.

        Parameters
        ----------
        table_name : str
            SQLite table name.

        Returns
        -------
        pandas.DataFrame
        """

        with self.connect() as conn:

            return pd.read_sql(
                f"SELECT * FROM {table_name}",
                conn
            )

    # ---------------------------------------------------------
    # Execute Custom Query
    # ---------------------------------------------------------

    def query(self, sql: str) -> pd.DataFrame:
        """
        Execute a custom SQL query.
        """

        with self.connect() as conn:

            return pd.read_sql(
                sql,
                conn
            )

    # ---------------------------------------------------------
    # Database Metadata
    # ---------------------------------------------------------

    def available_tables(self) -> pd.DataFrame:
        """
        Return all available tables.
        """

        return self.query(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name;
            """
        )

    # =========================================================
    # Convenience Methods
    # =========================================================

    def load_player_attributes(self):

        return self.load_table(
            "Player_Attributes"
        )

    def load_players(self):

        return self.load_table(
            "Player"
        )

    def load_matches(self):

        return self.load_table(
            "Match"
        )

    def load_teams(self):

        return self.load_table(
            "Team"
        )

    def load_team_attributes(self):

        return self.load_table(
            "Team_Attributes"
        )

    def load_leagues(self):

        return self.load_table(
            "League"
        )

    def load_countries(self):

        return self.load_table(
            "Country"
        )