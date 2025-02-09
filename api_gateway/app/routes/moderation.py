from fastapi import APIRouter, Request, Depends
from app.services.moderation import ModerationService
from app.core.rate_limiter import rate_limit

router = APIRouter()


def get_moderation_service():
    return ModerationService()


@router.post("/moderate")
async def proxy_moderation(
    request: Request,
    moderation_service: ModerationService = Depends(get_moderation_service),
    _: None = Depends(rate_limit(calls=10, period=60)),
):
    data = await request.json()
    return await moderation_service.moderate_text(data)
