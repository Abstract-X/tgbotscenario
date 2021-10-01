from typing import Dict, Set


class LockStorage:

    def __init__(self):

        self._storage: Dict[int, Set[int]] = {}

    def add_lock(self, *, chat_id: int, user_id: int) -> None:

        try:
            self._storage[chat_id].add(user_id)
        except KeyError:
            self._storage[chat_id] = {user_id}

    def remove_lock(self, *, chat_id: int, user_id: int) -> None:

        self._storage[chat_id].remove(user_id)
        if not self._storage[chat_id]:
            del self._storage[chat_id]

    def check_lock(self, *, chat_id: int, user_id: int) -> bool:

        try:
            return user_id in self._storage[chat_id]
        except KeyError:
            return False
