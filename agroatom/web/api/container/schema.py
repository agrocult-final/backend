from datetime import datetime
from typing import Optional

from pydantic import Field, root_validator, validator
from tortoise.contrib.pydantic import PydanticModel as BaseModel

from agroatom.db.models.yield_calculation_container import (
    YieldCalculationContainer,
    YieldCalculationContainerStatus,
)
from agroatom.db.models.yield_calculation_container_photo import (
    YieldCalculationContainerPhoto,
    YieldCalculationContainerPhotoStatus,
)


class YieldCalculationContainerCreateResponse(BaseModel):
    """Yield calculation container create response model."""

    id: int = Field(...)

    name: str = Field(...)

    note: Optional[str] = Field(default=None)
    planting_area: float = Field(..., gte=1)

    created_at: datetime = Field(...)
    calculated_at: Optional[datetime] = Field(default=None)

    grain_culture_id: Optional[int] = Field(default=None)

    coordinates: str = Field(...)

    average_weight_thousand_grains: Optional[float] = Field(..., gte=1)
    average_stems_per_meter: Optional[float] = Field(..., gte=1)

    status: YieldCalculationContainerStatus = Field(...)

    class Config:
        orm_mode = True
        orig_model = YieldCalculationContainer


class YieldCalculationContainerPhotoGetResponse(BaseModel):
    """Yield calculation container's photo get response model."""

    id: int = Field(...)

    file_name: str = Field(...)
    unique_file_name: str = Field(...)

    s3_path: str = Field(...)

    created_at: datetime = Field(...)
    calculated_at: Optional[datetime] = Field(default=None)

    container_id: int = Field(...)

    status: YieldCalculationContainerPhotoStatus = Field(...)

    class Config:
        orm_mode = True
        orig_model = YieldCalculationContainerPhoto


class YieldCalculationContainerGetResponse(BaseModel):
    """Yield calculation container get response model."""

    id: int = Field(...)

    note: Optional[str] = Field(default=None)
    planting_area: float = Field(..., gte=1)

    created_at: datetime = Field(...)
    calculated_at: Optional[datetime] = Field(default=None)

    grain_culture_id: Optional[int] = Field(default=None)

    average_weight_thousand_grains: Optional[float] = Field(..., gte=1)
    average_stems_per_meter: Optional[float] = Field(..., gte=1)
    biological_yield: Optional[float] = Field(..., gte=1)

    status: YieldCalculationContainerStatus = Field(...)

    class Config:
        orm_mode = True
        orig_model = YieldCalculationContainer


class YieldCalculationContainerCreateRequest(BaseModel):
    """Yield calculation container create request model."""

    name: str = Field(...)

    note: Optional[str] = Field(default=None)
    planting_area: float = Field(..., gte=1)

    coordinates: str = Field(...)

    grain_culture_id: Optional[int] = Field(default=None)

    custom_average_stems_per_meter: Optional[float] = Field(default=None, gte=1)
    custom_average_weight_thousand_grains: Optional[float] = Field(default=None, gte=1)

    @validator("coordinates")
    def validate_coordinates(cls, value: str) -> str:
        try:
            lt, lg = value.split(";")
            float(lt), float(lg)

        except (TypeError, ValueError):
            raise ValueError(
                "Invalid coordinates, example: 59.99099884033203;30.42118835449219",
            )

        return value

    @root_validator
    def check_average_weight_thousand_grains(cls, values):
        grain_culture, custom_average_weight_thousand_grains = (
            values.get(
                "grain_culture_id",
            ),
            values.get("custom_average_weight_thousand_grains"),
        )

        if not grain_culture and not custom_average_weight_thousand_grains:
            raise ValueError(
                "custom_average_weight_thousand_grains or grain_culture required",
            )

        return values

    class Config:
        orm_mode = True
        orig_model = YieldCalculationContainer
