from pydantic import UUID4
from celery import Celery
from loguru import logger
from app.services.moderation import ModerationService
from app.database.repository import ModerationRepository
import json

celery_app = Celery("tasks", broker="amqp://guest:guest@rabbitmq:5672/")
celery_app.config_from_object("app.tasks.celery_config")


@celery_app.task(
    bind=True,
    name="moderate_text_task",
    max_retries=3,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def moderate_text_task(self, text: str, moderation_id: UUID4):
    try:
        result = ModerationService.moderate_text(text=text)
        ModerationRepository.save_moderation_result(
            text=text,
            moderation_id=moderation_id,
            result=result["results"][0]["flagged"],
            meta=json.dumps(result),
        )
    except Exception as e:
        logger.error(f"Error in moderation task: {e}")
        delivery_info = self.request.delivery_info
        delivery_count = delivery_info.get("x-delivery-count", 1)

        if delivery_count >= 3:
            logger.error("Max retries reached. Moving to DLQ.")
            self.requeue = False
            raise
        else:
            logger.info(f"Retrying (attempt {delivery_count})...")
            raise self.retry(exc=e)
