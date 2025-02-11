from app.core.logging_config import setup_logging


def test_setup_logging():
    logger = setup_logging("test_service")
    assert logger is not None
