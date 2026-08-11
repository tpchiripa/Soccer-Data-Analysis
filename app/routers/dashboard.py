"""
Dashboard API
"""

from fastapi import APIRouter

from app.dependencies import player_service

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/stats")
def get_dashboard_stats():
    return {
        "players": len(player_service.players),
        "similarity_engine": "Ready",
        "api_status": "Online",
    }