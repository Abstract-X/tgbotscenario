from tgbotscenario.common.locks.storage import LockStorage
from tgbotscenario.common.locks.context import LockContext


class LockKeeper:

    def __init__(self):

        self._storage = LockStorage()

    def acquire(self, *, chat_id: int, user_id: int) -> LockContext:

        return LockContext(self._storage, chat_id=chat_id, user_id=user_id)

    def check(self, *, chat_id: int, user_id: int) -> bool:

        return self._storage.check(chat_id=chat_id, user_id=user_id)
