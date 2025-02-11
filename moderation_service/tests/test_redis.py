import pytest
import redis.asyncio as redis
from tenacity import retry, stop_after_attempt, wait_exponential


async def get_redis_client():
    return redis.from_url("redis://localhost:6379", decode_responses=True)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=10,
    ),
)
async def _redis_set(key: str, value: str, expiration: int = 60) -> bool:
    client = await get_redis_client()
    result = await client.set(key, value, ex=expiration)
    await client.aclose()
    return result


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=10,
    ),
)
async def set_redis_with_retry(
    key: str, value: str, expiration: int = 60
) -> bool:  # noqa
    return await _redis_set(key, value, expiration)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=10,
    ),
)
async def get_redis_with_retry(key: str) -> str:
    client = await get_redis_client()
    result = await client.get(key)
    await client.aclose()
    return result


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
async def delete_redis_with_retry(key: str) -> bool:
    client = await get_redis_client()
    result = await client.delete(key)
    await client.aclose()
    return bool(result)


@pytest.mark.asyncio
async def test_redis_operations():
    key = "test_key"
    value = "test_value"

    set_result = await set_redis_with_retry(key, value)
    assert set_result is True, "Failed to set redis value"

    retrieved_value = await get_redis_with_retry(key)
    assert (
        retrieved_value == value
    ), f"Expected {value}, but got {retrieved_value}"  # noqa

    delete_result = await delete_redis_with_retry(key)
    assert delete_result is True, "Failed to delete redis key"

    final_value = await get_redis_with_retry(key)
    assert final_value is None, "Key still exists after deletion"
