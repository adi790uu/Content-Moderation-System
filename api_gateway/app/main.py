from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import prometheus_client
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


@app.get("/metrics")
async def get_metrics():
    try:
        return Response(
            content=prometheus_client.generate_latest(),
            media_type="text/plain",
        )
    except Exception as e:
        logger.error(f"Error generating metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating metrics")


app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(moderation.router, prefix="/api", tags=["moderation"])
