import logging
from datetime import datetime

from tortoise import Tortoise

from agroatom.cv.utils import get_prediction
from agroatom.db.config import TORTOISE_CONFIG
from agroatom.db.models.yield_calculation_container_photo import (
    YieldCalculationContainerPhoto,
    YieldCalculationContainerPhotoStatus,
)
from agroatom.services.s3.storage import FileStorage

logger = logging.getLogger("actors.process_container_photos")


async def process_container_photo(photo_id: int):
    await Tortoise.init(config=TORTOISE_CONFIG)
    await Tortoise.generate_schemas()

    photo = await YieldCalculationContainerPhoto.get(pk=photo_id)

    try:
        if not photo or photo.status != YieldCalculationContainerPhotoStatus.processing:
            return None

        logger.info(
            "Containers #%s photo #%s processing!!!",
            (await photo.container).pk,
            photo.pk,
        )

        file = await FileStorage.get_temp_file(
            photo.unique_file_name,
            f"containers/photos/{(await photo.container).pk}",
        )

        logger.info(str(file))

        res = get_prediction(file.read())
        logger.info(str(res))
        res.render()
        logger.info(str(res))
        photo.average_grains_in_basket = (
            res.pandas().xyxy[0].shape[0] if res.pandas().xyxy else 0
        )
        photo.status = YieldCalculationContainerPhotoStatus.complete
        photo.calculated_at = datetime.now()

    except Exception:
        photo.status = YieldCalculationContainerPhotoStatus.internal_error
        logger.exception("Error on photo process!", exc_info=True)

    await photo.save()

    await Tortoise.close_connections()
