import pytest
from app.services.moderation import ModerationService
from unittest.mock import patch


@pytest.mark.asyncio
async def test_moderate_text():
    service = ModerationService()
    with patch(
        "app.external.openai.moderate_text",
        return_value={
            "result": True,
        },
    ):
        result = service.moderate_text("Sample text")
        assert result["result"] is True
