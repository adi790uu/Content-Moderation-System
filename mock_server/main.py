from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting the Mock Server")
        yield
        logger.info("Closing the Mock Server")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


def create_app() -> FastAPI:
    app = FastAPI(title="MOCK_SERVER", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_app()


MOCK_MODERATION_RESPONSE = {
    "id": "modr-970d409ef3bef3b70c73d8232df86e7d",
    "model": "omni-moderation-latest",
    "results": [
        {
            "flagged": True,
            "categories": {
                "sexual": False,
                "sexual/minors": False,
                "harassment": False,
                "harassment/threatening": False,
                "hate": False,
                "hate/threatening": False,
                "illicit": False,
                "illicit/violent": False,
                "self-harm": False,
                "self-harm/intent": False,
                "self-harm/instructions": False,
                "violence": True,
                "violence/graphic": False,
            },
            "category_scores": {
                "sexual": 2.34135824776394e-7,
                "sexual/minors": 1.6346470245419304e-7,
                "harassment": 0.0011643905680426018,
                "harassment/threatening": 0.0022121340080906377,
                "hate": 3.1999824407395835e-7,
                "hate/threatening": 2.4923252458203563e-7,
                "illicit": 0.0005227032493135171,
                "illicit/violent": 3.682979260160596e-7,
                "self-harm": 0.0011175734280627694,
                "self-harm/intent": 0.0006264858507989037,
                "self-harm/instructions": 7.368592981140821e-8,
                "violence": 0.8599265510337075,
                "violence/graphic": 0.37701736389561064,
            },
            "category_applied_input_types": {
                "sexual": ["image"],
                "sexual/minors": [],
                "harassment": [],
                "harassment/threatening": [],
                "hate": [],
                "hate/threatening": [],
                "illicit": [],
                "illicit/violent": [],
                "self-harm": ["image"],
                "self-harm/intent": ["image"],
                "self-harm/instructions": ["image"],
                "violence": ["image"],
                "violence/graphic": ["image"],
            },
        }
    ],
}


@app.post("/v1/moderations")
async def mock_moderation_api():
    try:
        asyncio.sleep(2)
        return MOCK_MODERATION_RESPONSE
    except Exception as e:
        logger.error(f"Error in moderation API: {e}")
        raise
