from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from loguru import logger


async def setup_rate_limiter(redis_url: str = "redis://localhost:6379"):
    try:
        redis_client = redis.from_url(redis_url)
        await FastAPILimiter.init(redis_client)
        logger.info("Rate limiter initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize rate limiter: {e}")
        raise


def rate_limit(calls: int = 10, period: int = 60):
    """
    Rate limiting dependency
    Args:
        calls: Number of calls allowed
        period: Time period in seconds
    """
    return RateLimiter(times=calls, seconds=period)
