import functools
import json
import hashlib
import datetime
import pendulum

from redis.asyncio.client import Redis
from redis.asyncio.cluster import RedisCluster
from redis import asyncio as aioredis

from fastapi.encoders import jsonable_encoder

from app.db.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession

from typing import (
    Dict,
    Callable,
    Optional,
    Union,
    Any,
)

import logging


logger = logging.getLogger("app")

CONVERTERS: Dict[str, Callable[[str], Any]] = {  # Логика декодирования особых типов
    "date": lambda x: pendulum.parse(x, exact=True),
    "datetime": lambda x: pendulum.parse(x, exact=True),
}


def object_hook(obj: Any) -> Any:
    _spec_type = obj.get("_spec_type")
    if not _spec_type:
        return obj

    if _spec_type in CONVERTERS:
        return CONVERTERS[_spec_type](obj["val"])
    else:
        raise TypeError(f"Unknown {_spec_type}")


class JsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        """добавляет метку поддерживаемым типам"""
        if isinstance(o, datetime.datetime):
            return {"val": str(o), "_spec_type": "datetime"}
        elif isinstance(o, datetime.date):
            return {"val": str(o), "_spec_type": "date"}
        else:
            return jsonable_encoder(o)


class JsonCoder:
    @classmethod
    def encode(cls, value: Any) -> Any:
        return json.dumps(value, cls=JsonEncoder).encode()

    @classmethod
    def decode(cls, value: bytes) -> Any:
        return json.loads(value.decode(), object_hook=object_hook)


class RedisCacheService:
    def __init__(self, redis: Union["Redis[bytes]", "RedisCluster[bytes]"]):
        self.redis = redis
        self.coder = JsonCoder

    async def get(self, key: str) -> Optional[bytes]:
        return await self.redis.get(key)

    async def set(self, key: str, value: bytes, expire: Optional[int] = None) -> None:
        await self.redis.set(key, value, ex=expire)


def args_normalise(kwargs: dict) -> dict:
    to_pop = []
    for key, value in kwargs.items():
        if isinstance(value, Base):
            kwargs[key] = value.id
        elif isinstance(value, AsyncSession):
            to_pop.append(key)
    for key in to_pop:
        kwargs.pop(key)


def cache(
    expire: int = 60,
    namespace: str = "",
):

    def wrapper(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):

            copy_kwargs = kwargs.copy()
            args_normalise(copy_kwargs)
            cache_key = hashlib.md5(  # noqa: S324
                f"{func.__module__}:{func.__name__}:{args}:{copy_kwargs}".encode()
            ).hexdigest()
            cache_key = namespace + cache_key
            logger.info(f"поиск в кеше запроса с ключом: {cache_key}")

            try:
                cached = await cache_service.get(cache_key)
            except Exception:
                logger.warning(
                    f"Не удалось найти ключ '{cache_key}' в кеше",
                    exc_info=True,
                )
                cached = None

            if cached is None:  # cache miss
                result = await func(*args, **kwargs)
                to_cache = cache_service.coder.encode(result)

                try:
                    await cache_service.set(cache_key, to_cache, expire)
                    logger.info(f"установка данныхв кеш с ключом: {cache_key}")
                except Exception as e:
                    logger.warning(
                        f"Ошибка установки ключа: '{cache_key}' в кеш: {e}",
                    )
            else:  # cache hit
                logger.info(f"cache hit: {cache_key}")
                result = cache_service.coder.decode(cached)

            return result

        return inner

    return wrapper


redis = aioredis.from_url("redis://localhost:6379")

cache_service = RedisCacheService(redis)
