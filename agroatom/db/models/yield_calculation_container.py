from enum import Enum

from tortoise import fields, models
from tortoise.validators import MinValueValidator


class YieldCalculationContainerStatus(Enum):
    """Enum of yield calculation container status."""

    created = "created"
    processing = "processing"
    complete = "complete"

    internal_error = "internal_error"

    def __repr__(self):
        return self.value


class YieldCalculationContainer(models.Model):
    """Model for yield calculation container purpose."""

    __slots__ = ("photos",)

    id = fields.IntField(pk=True)

    name = fields.CharField(max_length=255)
    note = fields.TextField(default=None, null=True)

    coordinates = fields.CharField(max_length=255)

    planting_area = fields.FloatField(validators=[MinValueValidator(min_value=1)])

    created_at = fields.DatetimeField(auto_now=True)
    calculated_at = fields.DatetimeField(null=True, default=None)

    grain_culture = fields.ForeignKeyField(
        "models.GrainCulture",
        related_name="containers",
        default=None,
        null=True,
        on_delete=fields.SET_NULL,
    )

    custom_average_weight_thousand_grains = fields.FloatField(
        validators=[MinValueValidator(min_value=1)],
        null=True,
        default=None,
    )

    status = fields.CharEnumField(
        YieldCalculationContainerStatus,
        default=YieldCalculationContainerStatus.created,
        max_length=200,
    )

    custom_average_stems_per_meter = fields.FloatField(
        validators=[MinValueValidator(min_value=1)],
        null=True,
        default=None,
    )

    biological_yield = fields.FloatField(
        validators=[MinValueValidator(min_value=0.0001)],
        null=True,
        default=None,
    )

    async def get_average_stems_per_meter(self) -> float:
        return (
            len(await self.photos.all())
            if len(await self.photos.all())
            else None
            if not self.custom_average_stems_per_meter
            else self.custom_average_stems_per_meter
        )

    async def get_average_weight_thousand_grains(self) -> float:
        return (
            (await self.grain_culture).average_weight_thousand_grains
            if not self.custom_average_weight_thousand_grains
            else self.custom_average_weight_thousand_grains
        )

    async def get_average_grains_in_basket(self) -> float:
        photos = await self.photos.all()
        return (
            sum(
                [
                    photo.average_grains_in_basket
                    for photo in photos
                    if photo.average_grains_in_basket
                ],
            )
            / len(photos)
        )

    def __str__(self) -> str:
        return self.created_at.isoformat()
