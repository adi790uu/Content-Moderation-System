from fastapi.testclient import TestClient
import pytest
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_proxy_moderation(client):
    response = client.post(
        "/api/moderate", json={"text": "Sample text for moderation."}
    )  # noqa
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_proxy_moderation_empty_text(client):
    response = client.post("/api/moderate", json={"text": ""})
    assert response.status_code == 400
    assert "Bad Request" in response.json()["error"]


def test_proxy_moderation_result(client):
    response = client.get("/api/result/2d19daba-653a-4137-8429-613268116b67")
    assert response.status_code in [200, 404]
