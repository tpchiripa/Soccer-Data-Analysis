"""
players.py

Player API endpoints.
"""

from fastapi import APIRouter, HTTPException

from app.dependencies import player_service

router = APIRouter(
    prefix="/players",
    tags=["Players"],
)


# ---------------------------------------------------------
# Search Players
# ---------------------------------------------------------

@router.get("/search")
def search_players(name: str):
    """
    Search players by name.

    Example:
        /players/search?name=Messi
    """

    results = player_service.search(name)

    return results.to_dict(orient="records")


# ---------------------------------------------------------
# Top Players
# ---------------------------------------------------------

@router.get("/top")
def top_players(limit: int = 20):
    """
    Return the highest-rated players.
    """

    results = player_service.top(limit)

    return results.to_dict(orient="records")


# ---------------------------------------------------------
# Player Profile
# ---------------------------------------------------------

@router.get("/{player_name}")
def player_profile(player_name: str):
    """
    Return a player by name.
    """

    results = player_service.search(player_name)

    if results.empty:
        raise HTTPException(
            status_code=404,
            detail="Player not found."
        )

    return results.iloc[0].to_dict()