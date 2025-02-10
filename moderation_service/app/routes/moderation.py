from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.moderation import ModerationService
from app.schemas.response import (
    ApiResponse,
    ModerationResultResponse,
    TextModerationReponse,
)
from loguru import logger
from app.tasks.moderation_tasks import moderate_text_task
import uuid
from pydantic import UUID4

from app.core.exceptions import RepositoryException
from app.schemas.request import ModerateTextRequest

router = APIRouter()


@router.post(
    "/v1/moderate/text",
)
async def moderate_text(request: ModerateTextRequest):
    try:
        moderation_id = uuid.uuid4()
        moderate_text_task.delay(request.text, moderation_id)
        return JSONResponse(
            status_code=200,
            content=ApiResponse(
                success=True,
                data=TextModerationReponse(
                    message="Task added",
                    moderation_id=moderation_id.hex,
                ),
            ).model_dump(),
        )
    except Exception as e:
        logger.error(e)
        return JSONResponse(
            status_code=500,
            content=ApiResponse(
                success=False,
                error=str(e),
            ).model_dump(),
        )


@router.get(
    "/v1/moderation/{id}",
)
async def get_moderation_results(id: UUID4):
    try:
        result = await ModerationService.get_moderation_results(id=id)
        return JSONResponse(
            status_code=200,
            content=ApiResponse(
                success=True,
                data=ModerationResultResponse(
                    message="Fetched result successfully!",
                    moderation_result=result,
                ),
            ).model_dump(),
        )
    except RepositoryException as e:
        logger.error(e)
        return JSONResponse(
            status_code=e.status_code,
            content=ApiResponse(
                success=False,
                data=None,
                error=str(e),
            ).model_dump(),
        )

    except Exception as e:
        logger.error(e)
        return JSONResponse(
            status_code=500,
            content=ApiResponse(
                success=False,
                error=str(e),
            ).model_dump(),
        )
