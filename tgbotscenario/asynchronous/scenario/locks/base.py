from __future__ import annotations
from abc import ABC, abstractmethod

from tgbotscenario import errors
import tgbotscenario.errors.lock_storage


class LockContext:

    __slots__ = ("_storage", "chat_id", "user_id")

    def __init__(self, storage: AbstractLockStorage, *, chat_id: int, user_id: int):

        self._storage = storage
        self.chat_id = chat_id
        self.user_id = user_id

    async def __aenter__(self):

        await self._storage.add(chat_id=self.chat_id, user_id=self.user_id)

    async def __aexit__(self, exc_type, exc_val, exc_tb):

        await self._storage.remove(chat_id=self.chat_id, user_id=self.user_id)


class AbstractLockStorage(ABC):

    @abstractmethod
    async def set(self, *, chat_id: int, user_id: int) -> None:

        pass

    @abstractmethod
    async def unset(self, *, chat_id: int, user_id: int) -> None:

        pass

    @abstractmethod
    async def check(self, *, chat_id: int, user_id: int) -> bool:

        pass

    def acquire(self, *, chat_id: int, user_id: int) -> LockContext:

        return LockContext(storage=self, chat_id=chat_id, user_id=user_id)

    async def add(self, *, chat_id: int, user_id: int) -> None:

        is_locked = await self.check(chat_id=chat_id, user_id=user_id)
        if is_locked:
            raise errors.lock_storage.TransitionLockExistsError(
                "transition lock already exists (chat_id={chat_id!r}, user_id={user_id!r})!",
                chat_id=chat_id, user_id=user_id
            )

        await self.set(chat_id=chat_id, user_id=user_id)

    async def remove(self, *, chat_id: int, user_id: int) -> None:

        await self.unset(chat_id=chat_id, user_id=user_id)
