"""
Comparison API Router
"""

from fastapi import APIRouter, HTTPException

from src.services.comparison_service import ComparisonService

router = APIRouter(
    prefix="/comparison",
    tags=["Comparison"]
)

service = ComparisonService("data/raw/database.sqlite")


@router.get("/")
def compare(player_one: str, player_two: str):

    try:

        basic = service.compare(
            player_one,
            player_two
        )

        attributes = service.compare_top_attributes(
            player_one,
            player_two
        )

        return {
            "comparison": basic.to_dict(orient="records"),
            "top_attributes": attributes.to_dict(orient="records")
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )