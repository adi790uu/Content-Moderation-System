import sys
from pathlib import Path
import time
from fastapi import FastAPI, Request
from loguru import logger


def log_request_time(app: FastAPI):
    @app.middleware("http")
    async def log_request(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"Request: {request.method} {request.url} - Processed in {process_time:.4f} seconds"  # noqa
        )
        return response

    return log_request


def setup_logging(service_name: str, log_level):
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
    return logger, log_request_time
