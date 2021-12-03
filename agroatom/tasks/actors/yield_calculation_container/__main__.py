from redis import Redis
from rq import Connection, Queue, Worker

from agroatom.settings import settings
from agroatom.tasks.actors.yield_calculation_container import (  # noqa
    process_container_photo,
    process_containers,
)

listen = ["high", "default", "low"]

conn = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_pass,
    username=settings.redis_user,
)

with Connection(conn):
    worker = Worker(map(Queue, listen))
    worker.work(logging_level="INFO")
