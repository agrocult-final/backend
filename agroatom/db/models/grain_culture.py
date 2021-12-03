from tortoise import fields, models
from tortoise.validators import MinValueValidator


class GrainCulture(models.Model):
    """Model for grain culture purpose."""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)  # noqa: WPS432
    average_weight_thousand_grains = fields.FloatField(
        validators=[MinValueValidator(min_value=1)],
    )

    def __str__(self) -> str:
        return self.name
