"""
Dashboard API
"""
from fastapi import APIRouter
from app.dependencies import player_service, watchlist_service

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/stats")
def get_dashboard_stats():
    top = player_service.top(limit=1)
    top_player = None
    if not top.empty:
        row = top.iloc[0]
        top_player = {
            "player_name": row["player_name"],
            "overall_rating": float(row["overall_rating"]),
        }

    watchlist_count = len(watchlist_service.list())

    return {
        "players": len(player_service.players),
        "watchlist_count": watchlist_count,
        "top_player": top_player,
    }