from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import UUID4
from app.schemas.api import ApiResponse
from app.core.exceptions import ServiceException
from app.services.moderation import ModerationService
from app.core.rate_limiter import rate_limit
from loguru import logger

router = APIRouter()


def get_moderation_service():
    return ModerationService()


@router.post("/moderate")
async def proxy_moderation(
    request: Request,
    moderation_service: ModerationService = Depends(get_moderation_service),
    _: None = Depends(rate_limit(calls=10, period=60)),
):
    try:
        data = await request.json()
        return await moderation_service.moderate_text(data)
    except ServiceException as e:
        logger.error(f"Moderation service health check failed: {str(e)}")
        return JSONResponse(
            status_code=e.status_code,
            content=ApiResponse(success=False, error=e.message).model_dump(),
        )
    except Exception as e:
        logger.error(
            f"Unexpected error during moderation service health check: {str(e)}"  # noqa
        )
        return JSONResponse(
            status_code=e.status_code,
            content=ApiResponse(success=False, error=e.message).model_dump(),
        )


@router.get("/result/{id}")
async def proxy_moderation_result(
    id: UUID4,
    moderation_service: ModerationService = Depends(get_moderation_service),
):
    try:
        response = await moderation_service.moderation_result(id=id)
        logger.info(response)
        return response
    except ServiceException as e:
        logger.error(f"Moderation service health check failed: {str(e)}")
        return JSONResponse(
            status_code=e.status_code,
            content=ApiResponse(success=False, error=e.message).model_dump(),
        )
    except Exception as e:
        logger.error(
            f"Unexpected error during moderation service health check: {str(e)}"  # noqa
        )
        return JSONResponse(
            status_code=e.status_code,
            content=ApiResponse(success=False, error=e.message).model_dump(),
        )
