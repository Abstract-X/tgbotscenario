import pytest

from tgbotscenario.asynchronous.states.storages.memory import MemoryStateStorage


class TestMemoryStateStorageLoad:

    @pytest.mark.asyncio
    async def test_chat_and_user_not_exists(self, chat_id, user_id):

        storage = MemoryStateStorage()
        states = await storage.load(chat_id=chat_id, user_id=user_id)

        assert states == []

    @pytest.mark.asyncio
    async def test_chat_and_user_exists(self, chat_id, user_id):

        storage = MemoryStateStorage()
        await storage.save(["InitialScene", "FooScene"], chat_id=chat_id, user_id=user_id)
        states = await storage.load(chat_id=chat_id, user_id=user_id)

        assert states == ["InitialScene", "FooScene"]

    @pytest.mark.asyncio
    async def test_source_mutability(self, chat_id, user_id):

        storage = MemoryStateStorage()
        source_states = ["InitialScene", "FooScene"]
        await storage.save(source_states, chat_id=chat_id, user_id=user_id)
        states = await storage.load(chat_id=chat_id, user_id=user_id)
        source_states.clear()

        assert states == ["InitialScene", "FooScene"]


class TestMemoryStateStorageSave:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id):

        storage = MemoryStateStorage()
        await storage.save(["InitialScene", "FooScene"], chat_id=chat_id, user_id=user_id)
        states = await storage.load(chat_id=chat_id, user_id=user_id)

        assert states == ["InitialScene", "FooScene"]

    @pytest.mark.asyncio
    async def test_storage_mutability(self, chat_id, user_id):

        storage = MemoryStateStorage()
        source_states = ["InitialScene", "FooScene"]
        await storage.save(source_states, chat_id=chat_id, user_id=user_id)
        source_states.clear()
        states = await storage.load(chat_id=chat_id, user_id=user_id)

        assert states == ["InitialScene", "FooScene"]
