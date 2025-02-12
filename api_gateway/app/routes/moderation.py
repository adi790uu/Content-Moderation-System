from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import UUID4
from app.schemas.request import ModerateTextPayload
from app.schemas.response import ApiResponse
from app.core.exceptions import ServiceException, ValidationException
from app.services.moderation import ModerationService
from app.core.rate_limiter import rate_limit
from loguru import logger
from app.core.metrics import REQUEST_COUNT

router = APIRouter()


def get_moderation_service():
    return ModerationService()


@router.post("/moderate")
async def proxy_moderation(
    request: ModerateTextPayload,
    moderation_service: ModerationService = Depends(get_moderation_service),
    _: None = Depends(rate_limit(calls=10, period=60)),
):
    try:
        REQUEST_COUNT.inc()
        if not request.text:
            raise ValidationException(
                message="Text cannot be empty",
                status_code=400,
            )
        return await moderation_service.moderate_text(request.text)
    except ValidationException as e:
        logger.error(f"Validation error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content=ApiResponse(
                success=False, error="Bad Request: " + str(e)
            ).model_dump(),
        )
    except ServiceException as e:
        logger.error(f"Moderation service failed: {str(e)}")
        return JSONResponse(
            status_code=e.status_code,
            content=ApiResponse(success=False, error=e.message).model_dump(),
        )
    except Exception as e:
        logger.error(f"Unexpected error during text moderation: {str(e)}")  # noqa
        return JSONResponse(
            status_code=500,
            content=ApiResponse(
                success=False,
                error="Internal Server Error",
            ).model_dump(),
        )


@router.get("/moderation/result/{id}")
async def proxy_moderation_result(
    id: UUID4,
    moderation_service: ModerationService = Depends(get_moderation_service),
    _: None = Depends(rate_limit(calls=10, period=60)),
):
    try:
        REQUEST_COUNT.inc()
        response = await moderation_service.moderation_result(id=id)
        return response
    except ServiceException as e:
        logger.error(f"{str(e)}")
        return JSONResponse(
            status_code=e.status_code,
            content=ApiResponse(success=False, error=e.message).model_dump(),
        )
    except Exception as e:
        logger.error(f"Unexpected error during fetching result: {str(e)}")  # noqa
        return JSONResponse(
            status_code=e.status_code,
            content=ApiResponse(success=False, error=e.message).model_dump(),
        )
