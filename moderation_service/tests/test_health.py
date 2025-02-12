from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)


def test_health_check():
    response = client.get(
        "/api/v1/health", headers={"X-Api-Gateway-Key": settings.GATEWAY_KEY}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "message" in response.json()["data"]
