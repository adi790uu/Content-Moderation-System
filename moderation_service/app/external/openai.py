import httpx
from app.core.config import settings


def moderate_text(text: str) -> dict:
    api_key = settings.OPENAI_API_KEY

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }  # noqa

    data = {"input": text}

    with httpx.Client() as client:
        response = client.post(
            "https://api.openai.com/v1/moderations", headers=headers, json=data
        )
        return response.json()
