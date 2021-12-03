from pydantic import BaseModel, Field


class GrainCultureResponse(BaseModel):
    """Grain culture response model."""

    id: int = Field(...)

    name: str = Field(...)
    average_weight_thousand_grains: float = Field(..., gt=1)

    class Config:
        orm_mode = True
