import pytest

from tgbotscenario.asynchronous.scenario.locks.storages.memory import MemoryLockStorage


class TestMemoryLockStorageSet:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id):

        storage = MemoryLockStorage()
        await storage.set(chat_id=chat_id, user_id=user_id)

        assert await storage.check(chat_id=chat_id, user_id=user_id)


class TestMemoryLockStorageUnset:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id):

        storage = MemoryLockStorage()
        await storage.set(chat_id=chat_id, user_id=user_id)
        await storage.unset(chat_id=chat_id, user_id=user_id)

        assert not await storage.check(chat_id=chat_id, user_id=user_id)


class TestMemoryLockStorageCheck:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id):

        storage = MemoryLockStorage()
        await storage.set(chat_id=chat_id, user_id=user_id)

        assert await storage.check(chat_id=chat_id, user_id=user_id)

        await storage.unset(chat_id=chat_id, user_id=user_id)

        assert not await storage.check(chat_id=chat_id, user_id=user_id)
