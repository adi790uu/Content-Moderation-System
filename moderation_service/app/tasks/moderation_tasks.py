from celery import Celery
from loguru import logger
from app.services.moderation import ModerationService
from app.database.repository import ModerationRepository
import json


celery_app = Celery("tasks", broker="redis://localhost:6379")


@celery_app.task(name="moderate_text_task")
def moderate_text_task(text: str):
    try:
        result = ModerationService.moderate_text(text=text)
        ModerationRepository.save_moderation_result(
            text=text,
            result=result["results"][0]["flagged"],
            meta=json.dumps(result),
        )
    except Exception as e:
        logger.error(f"Error in moderation task: {e}")
        raise
