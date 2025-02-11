from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_proxy_moderation():
    response = client.post(
        "/moderate", json={"text": "Sample text for moderation."}
    )  # noqa
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_proxy_moderation_empty_text():
    response = client.post("/moderate", json={"text": ""})
    assert response.status_code == 400
    assert "Bad Request" in response.json()["error"]


def test_proxy_moderation_result():
    response = client.get("/result/2d19daba-653a-4137-8429-613268116b67")
    assert response.status_code in [200, 404]
