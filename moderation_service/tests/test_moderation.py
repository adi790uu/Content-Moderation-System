from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)


def test_moderate_text():
    response = client.post(
        "/api/v1/moderate/text", json={"text": "Sample text for moderation."}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "moderation_id" in response.json()["data"]


def test_get_moderation_result():
    test_uuid = uuid4()
    response = client.get(f"/api/v1/moderation/{test_uuid}")
    assert response.status_code in [200, 404]
