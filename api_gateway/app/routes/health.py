from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, Response
from app.core.rate_limiter import rate_limit
from app.schemas.api import ApiResponse
from app.core.metrics import REQUEST_COUNT, HEALTH_STATUS
from app.core.exceptions import ServiceException
from app.services.moderation import ModerationService
import prometheus_client
from loguru import logger

router = APIRouter()


def get_moderation_service():
    return ModerationService()


@router.get("/health")
async def health_check():
    try:
        REQUEST_COUNT.inc()
        HEALTH_STATUS.set(1.0)
        api_response = ApiResponse(
            success=True,
            data={
                "message": "API Gateway is healthy",
            },
        )
        return JSONResponse(status_code=200, content=api_response.model_dump())
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        HEALTH_STATUS.set(0.0)
        raise HTTPException(
            status_code=500, detail="Internal server error during health check"
        )


@router.get("/health/moderation-service")
async def health_check_moderation_service(
    moderation_service: ModerationService = Depends(get_moderation_service),
    _: None = Depends(rate_limit(calls=10, period=60)),
):
    try:
        return await moderation_service.check_health()
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
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/metrics")
async def get_metrics():
    try:
        return Response(
            content=prometheus_client.generate_latest(),
            media_type="text/plain",
        )
    except Exception as e:
        logger.error(f"Error generating metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating metrics")
