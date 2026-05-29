from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "cyber_hub",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC"
)


import app.tasks.celery_tasks