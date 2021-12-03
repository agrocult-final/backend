from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException, Path

from agroatom.db.models.grain_culture import GrainCulture
from agroatom.web.api.grain_culture.schema import GrainCultureResponse

router = APIRouter()


@router.get("/", response_model=List[GrainCultureResponse])
async def get_grain_cultures() -> List[GrainCultureResponse]:
    response = [
        GrainCultureResponse.from_orm(grain_culture)
        async for grain_culture in GrainCulture.all()
    ]
    return response


@router.get("/{grain_culture_id}/", response_model=GrainCultureResponse)
async def get_grain_culture(
    grain_culture_id: int = Path(...),
) -> GrainCultureResponse:
    if grain_culture := await GrainCulture.get_or_none(
        pk=grain_culture_id,
    ):
        response = GrainCultureResponse.from_orm(grain_culture)
    else:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Grain culture not found!")

    return response
