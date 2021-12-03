from agroatom.tasks import get_rq_queue

queue = get_rq_queue()

from agroatom.tasks.actors.yield_calculation_container.container import (  # noqa
    process_containers,
)
from agroatom.tasks.actors.yield_calculation_container.container_photo import (  # noqa
    process_container_photo,
)
