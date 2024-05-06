from typing import Any, AsyncGenerator

from redis import asyncio as aioredis


async def get_redis(redis_url: str) -> AsyncGenerator[aioredis.Redis, Any]:
    redis = aioredis.from_url(url=redis_url, encoding="utf-8", decode_responses=True)  # type: ignore
    try:
        yield redis
    finally:
        await redis.close()
