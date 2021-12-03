from redis import Redis
from rq import Queue

from agroatom.settings import settings


def get_rq_queue():
    return Queue(
        connection=Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_pass,
            username=settings.redis_user,
        ),
    )
