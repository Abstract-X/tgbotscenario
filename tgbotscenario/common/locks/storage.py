from typing import FrozenSet


class LockStorage:

    def __init__(self):

        self._storage = {}

    @property
    def chat_ids(self) -> FrozenSet[int]:

        return frozenset(self._storage)

    def add(self, *, chat_id: int, user_id: int) -> None:

        try:
            self._storage[chat_id].add(user_id)
        except KeyError:
            self._storage[chat_id] = {user_id}

    def remove(self, *, chat_id: int, user_id: int) -> None:

        user_ids = self._storage[chat_id]
        user_ids.remove(user_id)
        if not user_ids:
            del self._storage[chat_id]

    def check(self, *, chat_id: int, user_id: int) -> bool:

        try:
            return user_id in self._storage[chat_id]
        except KeyError:
            return False
