from celery import Celery
from loguru import logger
from app.services.moderation import ModerationService

celery_app = Celery("tasks", broker="redis://localhost:6379")


@celery_app.task(name="moderate_text_task")
def moderate_text_task(text: str):
    try:
        result = ModerationService.moderate_text(text=text)
        return result
    except Exception as e:
        logger.error(f"Error in moderation task: {e}")
        raise
