from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import ServiceException
from app.schemas.api import ApiResponse
from loguru import logger
import time


async def error_handling_middleware(request: Request, call_next):
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.debug(f"Request processed in {process_time:.2f} seconds")
        return response
    except ServiceException as e:
        logger.error(f"Service exception: {str(e)}")
        return JSONResponse(
            status_code=e.status_code,
            content=ApiResponse(success=False, error=e.message).model_dump(),
        )
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        return JSONResponse(
            status_code=500,
            content=ApiResponse(
                success=False, error="Internal server error"
            ).model_dump(),
        )
