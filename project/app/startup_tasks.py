import os

from project.app.infrastructure.database import Base
from project.app.infrastructure.database.session import engine

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis


async def generate_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def generate_cache():
    redis = aioredis.from_url(os.environ.get("CACHE_URL"))
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
