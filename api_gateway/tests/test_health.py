from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.core.rate_limiter import rate_limit


async def override_rate_limit(calls: int = 10, period: int = 60):
    return None


app.dependency_overrides[rate_limit] = override_rate_limit


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "message" in response.json()["data"]


def test_health_check_moderation_service(client):
    response = client.get("/api/health/moderation-service")
    assert response.status_code in [200, 503]
