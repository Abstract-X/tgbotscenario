import json
from typing import List, TYPE_CHECKING

from tgbotscenario.asynchronous.states.storages.base import AbstractStateStorage

if TYPE_CHECKING:
    try:
        from aioredis import Redis
    except ModuleNotFoundError as e:
        import warnings

        warnings.warn("Install redis-py with `pip install aioredis`")
        raise e


class RedisStateStorage(AbstractStateStorage):
    def __init__(self, redis: Redis, prefix: str = "state_storage"):
        self._redis = redis
        self._prefix = prefix

    def get_key_name(self, user_id: int) -> str:
        return f"{self._prefix}-{user_id}"

    async def load(self, *, chat_id: int, user_id: int) -> List[str]:
        raw = await self._redis.hget(self.get_key_name(user_id), str(chat_id))
        return json.load(raw)

    async def save(self, states: List[str], *, chat_id: int, user_id: int) -> None:
        raw = json.dumps(states)
        await self._redis.hset(self.get_key_name(user_id), str(chat_id), raw)
