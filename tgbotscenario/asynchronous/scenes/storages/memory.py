from collections import defaultdict
from typing import List

from tgbotscenario.asynchronous.scenes.storages.base import AbstractSceneStorage


class MemorySceneStorage(AbstractSceneStorage):

    def __init__(self):
        self._storage = defaultdict(list)

    async def load_scenes(self, *, chat_id: int, user_id: int) -> List[str]:
        return self._storage[chat_id, user_id][:]

    async def save_scenes(self, scenes: List[str], *, chat_id: int, user_id: int) -> None:
        self._storage[chat_id, user_id] = scenes[:]
