from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tgbotscenario.asynchronous.scenario.locks.storages.base import AbstractLockStorage


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
