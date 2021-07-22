from tgbotscenario.synchronous.scenario.locks.storages.base import AbstractLockStorage


class MemoryLockStorage(AbstractLockStorage):

    def __init__(self):

        self._storage = {}

    def set(self, *, chat_id: int, user_id: int) -> None:

        try:
            self._storage[chat_id].add(user_id)
        except KeyError:
            self._storage[chat_id] = {user_id}

    def unset(self, *, chat_id: int, user_id: int) -> None:

        chat_users_ids: set = self._storage[chat_id]
        chat_users_ids.remove(user_id)
        if not chat_users_ids:
            del self._storage[chat_id]

    def check(self, *, chat_id: int, user_id: int) -> bool:

        try:
            return user_id in self._storage[chat_id]
        except KeyError:
            return False
