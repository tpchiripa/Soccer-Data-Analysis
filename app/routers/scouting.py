"""
Scouting API Router
"""

from fastapi import APIRouter, HTTPException

from app.dependencies import scouting_service

router = APIRouter(
    prefix="/scouting",
    tags=["Scouting"]
)


# ---------------------------------------------------------
# Scout Players
# ---------------------------------------------------------

@router.get("/")
def scout(
    min_overall: float | None = None,
    min_potential: float | None = None,
    preferred_foot: str | None = None,
    min_height: float | None = None,
    max_height: float | None = None,
    min_weight: float | None = None,
    max_weight: float | None = None,
    limit: int = 20,
):

    return scouting_service.scout(
        min_overall=min_overall,
        min_potential=min_potential,
        preferred_foot=preferred_foot,
        min_height=min_height,
        max_height=max_height,
        min_weight=min_weight,
        max_weight=max_weight,
        limit=limit,
    ).to_dict(orient="records")


# ---------------------------------------------------------
# Search by Attribute
# ---------------------------------------------------------

@router.get("/attribute/{attribute}")
def by_attribute(
    attribute: str,
    minimum: float,
    limit: int = 20,
):

    try:

        return scouting_service.by_attribute(
            attribute,
            minimum,
            limit,
        ).to_dict(orient="records")

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# ---------------------------------------------------------
# Elite Prospects
# ---------------------------------------------------------

@router.get("/elite")
def elite(
    potential: float = 90,
    overall: float = 75,
    limit: int = 20,
):

    return scouting_service.elite_prospects(
        potential=potential,
        overall=overall,
        limit=limit,
    ).to_dict(orient="records")