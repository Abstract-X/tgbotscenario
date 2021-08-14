from tgbotscenario.common.locks.storage import LockStorage
from tgbotscenario import errors
import tgbotscenario.errors.lock_keeper


class LockContext:

    __slots__ = ("_storage", "_chat_id", "_user_id")

    def __init__(self, storage: LockStorage, *, chat_id: int, user_id: int):

        self._storage = storage
        self._chat_id = chat_id
        self._user_id = user_id

    def __enter__(self):

        if self._storage.check(chat_id=self._chat_id, user_id=self._user_id):
            raise errors.lock_keeper.TransitionLockExistsError(
                "transition lock already exists (chat_id={chat_id!r}, user_id={user_id!r})!",
                chat_id=self._chat_id, user_id=self._user_id
            )

        self._storage.add(chat_id=self._chat_id, user_id=self._user_id)

    def __exit__(self, exc_type, exc_val, exc_tb):

        self._storage.remove(chat_id=self._chat_id, user_id=self._user_id)
