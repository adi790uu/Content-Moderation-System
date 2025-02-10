from typing import Any, Dict

from pydantic import UUID4
from app.core.exceptions import ModerationServiceException
from loguru import logger
import httpx


class ModerationService:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url

    async def check_health(self) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/health", timeout=5.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            logger.error(
                f"Timeout while connecting to moderation service at {self.base_url}"  # noqa
            )
            raise ModerationServiceException(
                "Moderation service timeout", status_code=504
            )
        except httpx.NetworkError:
            logger.error(
                f"Cannot connect to moderation service at {self.base_url}"
            )  # noqa
            raise ModerationServiceException(
                "Cannot connect to moderation service", status_code=503
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from moderation service: {str(e)}")
            raise ModerationServiceException(
                f"Moderation service error: {str(e)}",
                status_code=e.response.status_code,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error connecting to moderation service: {str(e)}"
            )  # noqa
            raise ModerationServiceException(
                "Internal server error",
                status_code=500,
            )

    async def moderate_text(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/moderate/text",
                    json=data,
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            logger.error("Timeout during text moderation request")
            raise ModerationServiceException(
                "Moderation request timeout", status_code=504
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during moderation: {str(e)}")
            raise ModerationServiceException(
                f"Moderation request failed: {str(e)}",
                status_code=e.response.status_code,
            )
        except Exception as e:
            logger.error(f"Unexpected error during moderation: {str(e)}")
            raise ModerationServiceException(
                "Internal server error",
                status_code=500,
            )

    async def moderation_result(self, id: UUID4) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/moderation/{id}",
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            logger.error("Timeout during fetching moderation results request")
            raise ModerationServiceException(
                "Moderation request timeout", status_code=504
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching moderation results: {str(e)}")
            raise ModerationServiceException(
                f"Moderation request failed: {str(e)}",
                status_code=e.response.status_code,
            )
        except Exception as e:
            logger.error(f"Unexpected error fetching moderation results: {str(e)}")
            raise ModerationServiceException(
                "Internal server error",
                status_code=500,
            )
