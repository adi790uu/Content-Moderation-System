from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import setup_logging
from app.routes import health, moderation
from app.core.rate_limiter import setup_rate_limiter
from app.core.middleware import error_handling_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger = setup_logging(service_name="api-gateway")
        logger.info("Starting the API gateway")
        await setup_rate_limiter()
        yield
        logger.info("Closing the API gateway")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


def create_app() -> FastAPI:
    app = FastAPI(title="API_GATEWAY", lifespan=lifespan)

    app.middleware("http")(error_handling_middleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, tags=["health"])
    app.include_router(moderation.router, tags=["moderation"])

    return app


app = create_app()
