from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6379")


@celery_app.task
def moderate_text_task(text: str):
    return "Done"
