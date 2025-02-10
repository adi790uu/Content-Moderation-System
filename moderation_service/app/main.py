from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logging_config import setup_logging
from .routes import moderation, health
from app.core import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger = setup_logging(service_name="moderation-service")
        logger.info("Starting the Moderation Service")
        yield
        logger.info("Closing the Moderation Service")
        await redis.close_redis_connection()
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


app = FastAPI(title="Moderation Service", lifespan=lifespan)

app.include_router(router=moderation.router, prefix="/api")
app.include_router(router=health.router, prefix="/api")
