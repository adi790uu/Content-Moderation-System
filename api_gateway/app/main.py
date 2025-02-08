from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from common.schemas.api import ApiResponse
from prometheus_client import Counter, Gauge
import prometheus_client
from common.logging.config import setup_logging
import requests

REQUEST_COUNT = Counter("api_requests_total", "Total number of API requests")
HEALTH_STATUS = Gauge(
    "api_health_status",
    "Health status of the API Gateway",
)

MODERATION_SERVICE_URL = "http://localhost:8001"


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger = setup_logging(service_name="api-gateway")
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


@app.post("/moderate")
async def proxy_moderation(request: Request):
    data = await request.json()
    response = requests.post(
        f"{MODERATION_SERVICE_URL}/api/v1/moderate/text", json=data
    )
    return response.json()
