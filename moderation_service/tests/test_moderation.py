from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from app.core.config import settings

client = TestClient(app)


class DummyTask:
    id = "dummy-task-id"


def fake_delay(*args, **kwargs):
    return DummyTask()


def test_moderate_text(monkeypatch):
    monkeypatch.setattr(
        "app.tasks.moderation_tasks.moderate_text_task.delay", fake_delay
    )
    response = client.post(
        "/api/v1/moderate/text",
        json={"text": "Sample text for moderation."},
        headers={"X-Api-Gateway-Key": settings.GATEWAY_KEY},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "moderation_id" in response.json()["data"]


def test_get_moderation_result():
    test_uuid = uuid4()
    response = client.get(
        f"/api/v1/moderation/{test_uuid}",
        headers={"X-Api-Gateway-Key": settings.GATEWAY_KEY},
    )
    assert response.status_code in [200, 404]
