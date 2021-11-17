import json
from typing import List, TYPE_CHECKING

from tgbotscenario.synchronous.states.storages.base import AbstractStateStorage

if TYPE_CHECKING:
    try:
        from redis.client import Redis
    except ModuleNotFoundError as e:
        import warnings

        warnings.warn("Install redis-py with `pip install redis-py`")
        raise e


class RedisStateStorage(AbstractStateStorage):
    def __init__(self, redis: Redis, prefix: str = "state_storage"):
        self._redis = redis
        self._prefix = prefix

    def get_key_name(self, user_id: int) -> str:
        return f"{self._prefix}-{user_id}"

    def load(self, *, chat_id: int, user_id: int) -> List[str]:
        raw = self._redis.hget(self.get_key_name(user_id), str(chat_id))
        return json.load(raw)

    def save(self, states: List[str], *, chat_id: int, user_id: int) -> None:
        raw = json.dumps(states)
        self._redis.hset(self.get_key_name(user_id), str(chat_id), raw)
