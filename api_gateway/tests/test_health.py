from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "message" in response.json()["data"]


def test_health_check_moderation_service():
    response = client.get("/health/moderation-service")
    assert response.status_code in [200, 503]
