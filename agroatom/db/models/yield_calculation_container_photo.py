from enum import Enum

from tortoise import fields, models
from tortoise.validators import MinValueValidator


class YieldCalculationContainerPhotoStatus(Enum):
    """Enum of yield calculation container's photo status."""

    uploaded = "uploaded"
    processing = "processing"
    complete = "complete"

    internal_error = "internal_error"

    def __repr__(self):
        return self.value


class YieldCalculationContainerPhoto(models.Model):
    """Model for yield calculation container's photo purpose."""

    id = fields.IntField(pk=True)
    file_name = fields.CharField(max_length=255)
    unique_file_name = fields.CharField(max_length=255)

    s3_path = fields.TextField()

    created_at = fields.DatetimeField(auto_now=True)
    calculated_at = fields.DatetimeField(null=True, default=None)

    status = fields.CharEnumField(
        YieldCalculationContainerPhotoStatus,
        default=YieldCalculationContainerPhotoStatus.uploaded,
        max_length=200,
    )

    container = fields.ForeignKeyField(
        "models.YieldCalculationContainer",
        related_name="photos",
        on_delete=fields.CASCADE,
    )

    average_grains_in_basket = fields.FloatField(
        validators=[MinValueValidator(min_value=1)],
        null=True,
        default=None,
    )
