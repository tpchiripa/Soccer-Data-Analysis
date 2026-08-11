"""
Similarity API Router
"""

from fastapi import APIRouter, HTTPException

from app.dependencies import similarity_service

router = APIRouter(
    prefix="/similarity",
    tags=["Similarity"]
)


# ---------------------------------------------------------
# Similar Players
# ---------------------------------------------------------

@router.get("/{player_name}")
def similar_players(player_name: str):
    """
    Return players with similar attributes.
    """

    try:

        return similarity_service.recommend(
            player_name
        ).to_dict(orient="records")

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )