from collections import defaultdict
from typing import List

from tgbotscenario.asynchronous.states.storages.base import AbstractStateStorage


class MemoryStateStorage(AbstractStateStorage):
    def __init__(self):
        self._storage = defaultdict(list)

    async def load(self, *, chat_id: int, user_id: int) -> List[str]:
        return self._storage[chat_id, user_id][:]

    async def save(self, states: List[str], *, chat_id: int, user_id: int) -> None:
        self._storage[chat_id, user_id] = states[:]
