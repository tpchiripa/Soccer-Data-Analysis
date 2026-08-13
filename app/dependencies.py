"""
dependencies.py

Shared application services for FootballIQ.

This module creates and exposes the application's core services
using a consistent dependency chain.
"""

from dotenv import load_dotenv

load_dotenv()

from src.data.download import ensure_database_exists
from src.services.player_service import PlayerService
from src.services.profile_service import PlayerProfileService
from src.services.similarity_service import SimilarityService
from src.services.comparison_service import ComparisonService
from src.services.scouting_service import ScoutingService
from src.services.watchlist_service import WatchlistService
from src.services.auth_service import AuthService


# ============================================================
# Configuration
# ============================================================

DB_PATH = "data/raw/database.sqlite"

ensure_database_exists(DB_PATH)


# ============================================================
# Core Services
# ============================================================

player_service = PlayerService(DB_PATH)


# ============================================================
# Business Services
# ============================================================

profile_service = PlayerProfileService(
    player_service
)

similarity_service = SimilarityService(
    player_service
)

comparison_service = ComparisonService(
    profile_service
)

scouting_service = ScoutingService(
    player_service
)

watchlist_service = WatchlistService(
    player_service,
    DB_PATH
)

auth_service = AuthService(
    DB_PATH
)