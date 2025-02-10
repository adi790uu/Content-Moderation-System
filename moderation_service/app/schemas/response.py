from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class ApiResponse(Generic[T], BaseModel):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    message: str


class TextModerationReponse(BaseModel):
    message: str
    moderation_id: str


class ModerationResultResponse(BaseModel):
    moderation_result: bool
    message: str
