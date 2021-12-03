import typer
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from rq import Retry

from agroatom.tasks import get_rq_queue
from agroatom.tasks.actors.yield_calculation_container import process_containers


def start_worker(start_scheduler: bool = True):
    queue = get_rq_queue()

    if start_scheduler:
        scheduler = BlockingScheduler()
        scheduler.add_job(
            lambda: queue.enqueue(process_containers, retry=Retry(max=3)),
            IntervalTrigger(seconds=2),
        )
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()


if __name__ == "__main__":
    typer.run(start_worker)
