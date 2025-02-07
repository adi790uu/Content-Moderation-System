from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from common.models import ApiResponse


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
    api_response = ApiResponse(
        success=True,
        data={
            "message": "API Gateway is healthy",
        },
    )
    return JSONResponse(status_code=200, content=api_response.model_dump())
