from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.common.logging.config import setup_logging
from .routes import moderation, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger = setup_logging(service_name="moderation-service")
        logger.info("Starting the API gateway")
        yield
        logger.info("Closing the API gateway")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


app = FastAPI(title="Moderation Service", lifespan=lifespan)

app.include_router(router=moderation.router, prefix="/api")
app.include_router(router=health.router, prefix="/api")
