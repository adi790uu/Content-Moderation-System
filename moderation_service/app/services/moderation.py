import app.external.openai as openai_service
from pydantic import UUID4
from app.database.repository import ModerationRepository
from app.core import redis
from loguru import logger


class ModerationService:
    @staticmethod
    def moderate_text(text: str):
        result = openai_service.moderate_text(text=text)
        return result

    @staticmethod
    async def get_moderation_results(id: UUID4):
        cached_result: str = await redis.get_redis_with_retry(
            key=f"moderation_id:{id}",
        )
        logger.info(cached_result)
        if cached_result:
            return cached_result
        moderation_result: bool = (
            await ModerationRepository.get_moderation_result_by_uuid(
                uuid=id,
            )
        )
        await redis.set_redis_with_retry(
            key=f"moderation_id:{id}",
            value=str(moderation_result),
        )
        return moderation_result
