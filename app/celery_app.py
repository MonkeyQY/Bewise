from celery import Celery

from app import config

app_celery = Celery(__name__, include=["app.tasks"])
app_celery.conf.broker_url = (
    f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/0"
)
app_celery.conf.result_backend = (
    f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/0"
)
app_celery.conf.max_loop_interval = 60 * 320
app_celery.conf.worker_disable_rate_limits = True
