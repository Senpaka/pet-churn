from celery import Celery
import os
import dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
dotenv.load_dotenv(BASE_DIR / ".env")

print(BASE_DIR)

app = Celery(
    "BackGround tasks",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL"),
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