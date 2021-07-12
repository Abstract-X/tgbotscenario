from typing import List

from tgbotscenario.asynchronous.states.storages.base import AbstractStateStorage


class MemoryStateStorage(AbstractStateStorage):

    def __init__(self):

        self._storage = {}

    async def load(self, *, chat_id: int, user_id: int) -> List[str]:

        try:
            states = self._storage[chat_id][user_id][:]
        except KeyError:
            states = []

        return states

    async def save(self, states: List[str], *, chat_id: int, user_id: int) -> None:

        try:
            users_ids = self._storage[chat_id]
        except KeyError:
            self._storage[chat_id] = users_ids = {}

        users_ids[user_id] = states[:]
