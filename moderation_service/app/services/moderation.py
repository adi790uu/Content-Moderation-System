import app.external.openai as openai_service
from pydantic import UUID4

from app.database.repository import ModerationRepository


class ModerationService:
    @staticmethod
    def moderate_text(text: str):
        result = openai_service.moderate_text(text=text)
        return result

    @staticmethod
    async def get_moderation_results(id: UUID4):
        moderation_result = await ModerationRepository.get_moderation_result_by_uuid(
            uuid=id
        )
        return moderation_result.result
