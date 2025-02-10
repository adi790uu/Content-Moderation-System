from fastapi import APIRouter
from app.services.moderation import ModerationService
from app.common.schemas.api import ApiResponse
from pydantic import BaseModel
from loguru import logger
from app.tasks.moderation_tasks import moderate_text_task
import uuid
from pydantic import UUID4

router = APIRouter()


class ModerateTextRequest(BaseModel):
    text: str


class SampleReponse(BaseModel):
    message: str
    moderation_id: UUID4


class ModerationResult(BaseModel):
    moderation_result: bool
    message: str


@router.post(
    "/v1/moderate/text",
    response_model=ApiResponse[SampleReponse],
)
async def moderate_text(request: ModerateTextRequest):
    try:
        moderation_id = uuid.uuid4()
        moderate_text_task.delay(request.text, moderation_id)
        return ApiResponse(
            success=True,
            data=SampleReponse(
                message="Task added",
                moderation_id=moderation_id,
            ),
        )
    except Exception as e:
        logger.error(e)
        return ApiResponse(success=False, error=str(e))


@router.get(
    "/v1/moderation/{id}",
    response_model=ApiResponse[ModerationResult],
)
async def get_moderation_results(id: UUID4):
    try:
        result = await ModerationService.get_moderation_results(id=id)
        logger.info(result)
        return ApiResponse(
            success=True,
            data=ModerationResult(
                message="Fetched result successfully!",
                moderation_result=result,
            ),
        )
    except Exception as e:
        logger.error(e)
