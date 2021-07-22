from abc import ABC, abstractmethod

from tgbotscenario.synchronous.scenario.locks.context import LockContext
from tgbotscenario import errors
import tgbotscenario.errors.lock_storage


class AbstractLockStorage(ABC):

    @abstractmethod
    def set(self, *, chat_id: int, user_id: int) -> None:

        pass

    @abstractmethod
    def unset(self, *, chat_id: int, user_id: int) -> None:

        pass

    @abstractmethod
    def check(self, *, chat_id: int, user_id: int) -> bool:

        pass

    def acquire(self, *, chat_id: int, user_id: int) -> LockContext:

        return LockContext(storage=self, chat_id=chat_id, user_id=user_id)

    def add(self, *, chat_id: int, user_id: int) -> None:

        is_locked = self.check(chat_id=chat_id, user_id=user_id)
        if is_locked:
            raise errors.lock_storage.TransitionLockExistsError(
                "transition lock already exists (chat_id={chat_id!r}, user_id={user_id!r})!",
                chat_id=chat_id, user_id=user_id
            )

        self.set(chat_id=chat_id, user_id=user_id)

    def remove(self, *, chat_id: int, user_id: int) -> None:

        self.unset(chat_id=chat_id, user_id=user_id)
