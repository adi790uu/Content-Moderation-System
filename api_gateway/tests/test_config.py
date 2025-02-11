from app.core.config import settings


def test_settings():
    assert settings.REDIS_URL is not None
