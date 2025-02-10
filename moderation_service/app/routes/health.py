from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.common.schemas.api import ApiResponse
from loguru import logger


router = APIRouter()


class HealthResponse(BaseModel):
    message: str


@router.get(
    "/v1/health",
)
async def get_moderation_service_health():
    try:
        return JSONResponse(
            status_code=200,
            content=ApiResponse(
                success=True,
                data=HealthResponse(
                    message="Service is healthy",
                ),
            ).model_dump(),
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=500,
            content=ApiResponse(
                success=False,
                error="Service is unhealthy",
            ).model_dump(),
        )
