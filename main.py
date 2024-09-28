from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from contextlib import asynccontextmanager

from redis import asyncio as aioredis

from app.config import settings

from app.routes.dialogs.router import router as dialogs_router
from app.routes.users.router import router as users_router
from app.routes.managers.router import router as managers_router


@asynccontextmanager
async def lifespan(_: FastAPI):

    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    await redis.close()


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(dialogs_router)
app.include_router(managers_router)


