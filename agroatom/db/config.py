from typing import List

from agroatom.settings import settings

MODELS_MODULES: List[str] = [
    "agroatom.db.models.grain_culture",
    "agroatom.db.models.yield_calculation_container",
    "agroatom.db.models.yield_calculation_container_photo",
]

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": ["aerich.models"] + MODELS_MODULES,
            "default_connection": "default",
        },
    },
}
