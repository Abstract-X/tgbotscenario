from tgbotscenario.common.transitions.locks.storage import LockStorage
from tgbotscenario import errors


class LockContext:
    __slots__ = ("_storage", "_chat_id", "_user_id")

    def __init__(self, storage: LockStorage, *, chat_id: int, user_id: int):
        self._storage = storage
        self._chat_id = chat_id
        self._user_id = user_id

    def __enter__(self):
        if self._storage.check_lock(chat_id=self._chat_id, user_id=self._user_id):
            raise errors.LockExistsError(
                "lock already exists (chat_id={chat_id!r}, user_id={user_id!r})!",
                chat_id=self._chat_id, user_id=self._user_id
            )
        self._storage.add_lock(chat_id=self._chat_id, user_id=self._user_id)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._storage.remove_lock(chat_id=self._chat_id, user_id=self._user_id)
