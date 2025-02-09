from fastapi import APIRouter
from app.common.schemas.api import ApiResponse
from pydantic import BaseModel
from loguru import logger


router = APIRouter()


class SampleReponse(BaseModel):
    message: str


@router.get(
    "/v1/health",
    response_model=ApiResponse[SampleReponse],
)
async def get_moderation_service_health():
    try:
        return ApiResponse(
            success=True, data=SampleReponse(message="Service is healthy")
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return ApiResponse(
            success=False,
            error="Service is unhealthy",
            data=SampleReponse(message="Service is unhealthy"),
        )
