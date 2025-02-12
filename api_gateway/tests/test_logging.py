from app.core.logging_config import setup_logging
from app.core.config import settings


def test_setup_logging():
    logger = setup_logging("test_service", log_level=settings.LOG_LEVEL)
    assert logger is not None
