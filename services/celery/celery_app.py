from celery import Celery

from core.settings import settings

"""
Настройка Celery 
"""

app = Celery(
    "BackGround tasks",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    imports=("services.celery.tasks",)
)