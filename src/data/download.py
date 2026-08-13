"""
download.py
Ensures the player database exists locally, downloading it from a
remote source (e.g. a GitHub Release asset) if it's missing — used
on fresh deploys where the large SQLite file isn't committed to git.
"""

from __future__ import annotations

import os
from pathlib import Path

import requests

DATABASE_URL = (
    "https://github.com/tpchiripa/Soccer-Data-Analysis/"
    "releases/download/data-v2-demo/database_demo.sqlite"
)


def ensure_database_exists(db_path: str) -> None:
    """
    Download the database file if it doesn't already exist locally.
    """
    path = Path(db_path)

    if path.exists():
        return

    print(f"Database not found at {db_path}. Downloading...")

    path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(DATABASE_URL, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))
    downloaded = 0

    with open(path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total_size:
                percent = (downloaded / total_size) * 100
                print(f"\rDownloading: {percent:.1f}%", end="")

    print("\nDatabase downloaded successfully.")