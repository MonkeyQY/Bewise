import logging

from app.celery_app import app_celery

log = logging.getLogger("Celery task")


@app_celery.on_after_configure.connect
def create_period_task(sender=app_celery, **kwargs):
    pass


@app_celery.task
def start_celery_task(nm_id: int) -> None:
    pass
