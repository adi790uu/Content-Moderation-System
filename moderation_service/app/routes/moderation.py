from fastapi import APIRouter
from app.common.schemas.api import ApiResponse
from pydantic import BaseModel
from loguru import logger
from app.tasks.moderation_tasks import moderate_text_task

router = APIRouter()


class ModerateTextRequest(BaseModel):
    text: str


class SampleReponse(BaseModel):
    message: str
    # task_id: int | str


@router.post(
    "/v1/moderate/text",
    response_model=ApiResponse[SampleReponse],
)
async def moderate_text(request: ModerateTextRequest):
    try:
        moderate_text_task.delay(request.text)
        return ApiResponse(
            success=True,
            data=SampleReponse(
                message="Task added",
                # task_id=task.id,
            ),
        )
    except Exception as e:
        logger.error(e)
        return ApiResponse(success=False, error=str(e))


@router.get(
    "/v1/moderation/{moderation_id}",
    response_model=ApiResponse[SampleReponse],
)
async def get_moderation_results(moderation_id: int):
    try:
        pass
    except Exception as e:
        logger.error(e)
