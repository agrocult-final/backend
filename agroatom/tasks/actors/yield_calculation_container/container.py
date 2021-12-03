import logging
from datetime import datetime

from rq import Retry
from tortoise import Tortoise

from agroatom.db.config import TORTOISE_CONFIG
from agroatom.db.models.yield_calculation_container import (
    YieldCalculationContainer,
    YieldCalculationContainerStatus,
)
from agroatom.db.models.yield_calculation_container_photo import (
    YieldCalculationContainerPhotoStatus,
)
from agroatom.tasks.actors.yield_calculation_container import queue
from agroatom.tasks.actors.yield_calculation_container.container_photo import (
    process_container_photo,
)

logger = logging.getLogger("actors.process_containers")


async def process_containers():
    await Tortoise.init(config=TORTOISE_CONFIG)
    await Tortoise.generate_schemas()

    async for container in YieldCalculationContainer.filter(
        status=YieldCalculationContainerStatus.processing,
    ):
        for_complete = True

        logger.info("Container #%s on processing", container.pk)

        async for photo in container.photos.all():
            logger.info(
                "Containers #%s photo #%s on status check",
                container.pk,
                photo.pk,
            )

            if photo.status == YieldCalculationContainerPhotoStatus.uploaded:
                logger.info(
                    "Containers #%s photo #%s start processing",
                    container.pk,
                    photo.pk,
                )

                for_complete = False

                photo.status = YieldCalculationContainerStatus.processing
                await photo.save()

                queue.enqueue(process_container_photo, photo.pk, retry=Retry(max=3))

            elif photo.status == YieldCalculationContainerPhotoStatus.processing:
                logger.info(
                    "Containers #%s photo #%s on processing",
                    container.pk,
                    photo.pk,
                )
                for_complete = False

            elif photo.status == YieldCalculationContainerPhotoStatus.internal_error:
                logger.info(
                    "Containers #%s photo #%s fault",
                    container.pk,
                    photo.pk,
                )
                container.status = YieldCalculationContainerStatus.internal_error

        if (
            for_complete
            and container.status != YieldCalculationContainerStatus.internal_error
        ):
            logger.info("Container #%s finish calculations", container.pk)

            container.calculated_at = datetime.now()
            container.biological_yield = (
                await container.get_average_stems_per_meter()
                * await container.get_average_grains_in_basket()
                * await container.get_average_weight_thousand_grains()
            ) / 1e5  # meters -> hectares, grams -> hundredweight.

            container.status = YieldCalculationContainerStatus.complete

        await container.save()

    await Tortoise.close_connections()
