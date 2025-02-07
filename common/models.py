from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class ApiResponse(Generic[T], BaseModel):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
