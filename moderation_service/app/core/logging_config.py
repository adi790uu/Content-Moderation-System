import sys
from pathlib import Path
from loguru import logger


def setup_logging(service_name: str, log_level: str = "INFO"):
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True, parents=True)

    logger.remove()

    log_format = (
        f"{{time:YYYY-MM-DD HH:mm:ss}} [{{level}}] {service_name} - {{message}}"  # noqa
    )

    logger.add(
        sys.stdout,
        level="DEBUG",
        format=log_format,
    )

    logger.add(
        log_dir / f"{service_name}.log",
        level=log_level,
        rotation="10 MB",
        retention="5 days",
        encoding="utf8",
        format=log_format,
    )

    logger.info(f"Logging initialized for service: {service_name}")
    return logger
