from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_metrics():
    response = client.get("/api/metrics")
    assert response.status_code == 200
    assert "api_requests_total" in response.text
