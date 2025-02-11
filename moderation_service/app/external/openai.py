import httpx
from app.core.config import settings


def moderate_text(text: str) -> dict:
    headers = {
        "Content-Type": "application/json",
    }
    data = {"input": text}

    with httpx.Client() as client:
        response = client.post(
            f"{settings.TEXT_MODERATION_API}/v1/moderations",
            headers=headers,
            json=data,
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()
