"""
dependencies.py

Shared application services for FootballIQ.
"""

from src.services.player_service import PlayerService
from src.services.profile_service import PlayerProfileService
from src.services.similarity_service import SimilarityService
from src.services.comparison_service import ComparisonService
from src.services.scouting_service import ScoutingService

# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

DB_PATH = "data/raw/database.sqlite"

# ---------------------------------------------------------
# Core Service
# ---------------------------------------------------------

player_service = PlayerService(DB_PATH)

# ---------------------------------------------------------
# Business Services
# ---------------------------------------------------------

profile_service = PlayerProfileService(player_service)

similarity_service = SimilarityService(player_service)

comparison_service = ComparisonService(player_service)

scouting_service = ScoutingService(player_service)