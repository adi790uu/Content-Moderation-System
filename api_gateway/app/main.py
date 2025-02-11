from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_config import setup_logging, log_request_time
from app.routes import health, moderation
from app.core.rate_limiter import setup_rate_limiter
from contextlib import asynccontextmanager
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting the API gateway")
    await setup_rate_limiter()
    yield
    logger.info("Closing the API gateway")


app = FastAPI(title="API_GATEWAY", lifespan=lifespan)

logger, _ = setup_logging(
    service_name="api-gateway",
    log_level=settings.LOG_LEVEL,
)
log_request_time(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router, tags=["health"])
app.include_router(moderation.router, tags=["moderation"])
