"""
build_demo_db.py
Creates a smaller SQLite database containing only the top-rated players,
for deployment on memory-constrained hosting (e.g. Render's free tier).
"""

import os
import sqlite3

SOURCE_DB = "data/raw/database.sqlite"
OUTPUT_DB = "data/raw/database_demo.sqlite"
TOP_N_PLAYERS = 2000

if os.path.exists(OUTPUT_DB):
    os.remove(OUTPUT_DB)

source_conn = sqlite3.connect(SOURCE_DB)
dest_conn = sqlite3.connect(OUTPUT_DB)

# Find the top N players by their most recent overall_rating.
top_players = source_conn.execute(
    """
    SELECT player_api_id
    FROM Player_Attributes
    WHERE (player_api_id, date) IN (
        SELECT player_api_id, MAX(date)
        FROM Player_Attributes
        GROUP BY player_api_id
    )
    ORDER BY overall_rating DESC
    LIMIT ?
    """,
    (TOP_N_PLAYERS,),
).fetchall()

player_ids = [row[0] for row in top_players]
print(f"Selected {len(player_ids)} players.")

placeholders = ",".join("?" for _ in player_ids)

# Copy schema for both tables.
player_schema = source_conn.execute(
    "SELECT sql FROM sqlite_master WHERE type='table' AND name='Player'"
).fetchone()[0]

attrs_schema = source_conn.execute(
    "SELECT sql FROM sqlite_master WHERE type='table' AND name='Player_Attributes'"
).fetchone()[0]

dest_conn.execute(player_schema)
dest_conn.execute(attrs_schema)

# Copy filtered rows for Player.
player_cols = [
    row[1] for row in source_conn.execute("PRAGMA table_info(Player)").fetchall()
]
players_rows = source_conn.execute(
    f"SELECT * FROM Player WHERE player_api_id IN ({placeholders})",
    player_ids,
).fetchall()
dest_conn.executemany(
    f"INSERT INTO Player VALUES ({','.join('?' for _ in player_cols)})",
    players_rows,
)

# Copy filtered rows for Player_Attributes.
attr_cols = [
    row[1]
    for row in source_conn.execute(
        "PRAGMA table_info(Player_Attributes)"
    ).fetchall()
]
attrs_rows = source_conn.execute(
    f"SELECT * FROM Player_Attributes WHERE player_api_id IN ({placeholders})",
    player_ids,
).fetchall()
dest_conn.executemany(
    f"INSERT INTO Player_Attributes VALUES ({','.join('?' for _ in attr_cols)})",
    attrs_rows,
)

dest_conn.commit()
dest_conn.close()
source_conn.close()

print(f"Demo database written to {OUTPUT_DB}")