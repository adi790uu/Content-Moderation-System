from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ApiResponse
import uvicorn
from prometheus_client import Counter, Gauge
import prometheus_client

REQUEST_COUNT = Counter("api_requests_total", "Total number of API requests")
HEALTH_STATUS = Gauge(
    "api_health_status",
    "Health status of the API Gateway",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting the API gateway")
        yield
        logger.info("Closing the API gateway")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


app = FastAPI(title="API_GATEWAY", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    REQUEST_COUNT.inc()
    HEALTH_STATUS.set(1.0)
    api_response = ApiResponse(
        success=True,
        data={
            "message": "API Gateway is healthy",
        },
    )
    return JSONResponse(status_code=200, content=api_response.model_dump())


@app.get("/metrics")
async def get_metrics():
    return Response(
        content=prometheus_client.generate_latest(),
        media_type="text/plain",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
