import redis.asyncio as aioredis
from app.config.settings import settings


redis_connection = aioredis.from_url(settings.REDIS_SESSION_URL, decode_responses=True)