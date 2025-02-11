from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from app.core.logging_config import setup_logging, log_request_time
from .routes import moderation, health
from app.core import redis
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting the Moderation Service")
        yield
        logger.info("Closing the Moderation Service")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        await redis.close_redis_connection()


app = FastAPI(title="Moderation Service", lifespan=lifespan)

logger, _ = setup_logging(service_name="moderation_service")
log_request_time(app)


@app.middleware("http")
async def validate_gateway_header(request: Request, call_next):
    API_GATEWAY_HEADER = "X-Api-Gateway-Key"
    header_value = request.headers.get(API_GATEWAY_HEADER)
    if header_value != settings.GATEWAY_KEY:
        raise HTTPException(
            status_code=403, detail="Access forbidden: Invalid gateway header"
        )
    response = await call_next(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.API_GATEWAY_DOMAIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=moderation.router, prefix="/api")
app.include_router(router=health.router, prefix="/api")
