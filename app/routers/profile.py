"""
profile.py

Player Profile API.
"""

from fastapi import APIRouter, HTTPException

from app.dependencies import profile_service

router = APIRouter(
    prefix="/profile",
    tags=["Player Profile"],
)


@router.get("/{player_name}")
def get_player_profile(player_name: str):
    """
    Return a detailed player profile.
    """
    try:
        return profile_service.get_profile(player_name)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )