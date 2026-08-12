"""
Watchlist API Router
"""
from fastapi import APIRouter, HTTPException
from app.dependencies import watchlist_service

router = APIRouter(
    prefix="/watchlist",
    tags=["Watchlist"]
)


@router.get("/")
def list_watchlist():
    """
    Return all players currently on the watchlist.
    """
    return watchlist_service.list().to_dict(orient="records")


@router.post("/{player_api_id}")
def add_to_watchlist(player_api_id: int, note: str = ""):
    """
    Add a player to the watchlist.
    """
    try:
        return watchlist_service.add(player_api_id, note)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{player_api_id}")
def remove_from_watchlist(player_api_id: int):
    """
    Remove a player from the watchlist.
    """
    return watchlist_service.remove(player_api_id)