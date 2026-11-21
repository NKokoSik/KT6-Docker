import os

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("kt6_tasks", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(name="tasks.send_welcome_email")
def send_welcome_email(email: str, username: str):
    message = f"Welcome message prepared for {username} ({email})"
    print(message, flush=True)
    return {"sent": True, "email": email, "message": message}
