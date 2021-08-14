import pytest

from tgbotscenario.asynchronous.scenes.storages.memory import MemorySceneStorage


class TestMemorySceneStorageLoad:

    @pytest.mark.asyncio
    async def test_scenes_not_exists(self, chat_id, user_id):

        storage = MemorySceneStorage()

        assert await storage.load(chat_id=chat_id, user_id=user_id) == []

    @pytest.mark.asyncio
    async def test_scenes_exists(self, chat_id, user_id):

        storage = MemorySceneStorage()
        scenes = ["InitialScene", "Scene"]
        await storage.save(scenes, chat_id=chat_id, user_id=user_id)

        assert await storage.load(chat_id=chat_id, user_id=user_id) == scenes

    @pytest.mark.asyncio
    async def test_mutability(self, chat_id, user_id):

        storage = MemorySceneStorage()
        scenes = ["InitialScene", "Scene"]
        await storage.save(scenes, chat_id=chat_id, user_id=user_id)

        loaded_scenes = await storage.load(chat_id=chat_id, user_id=user_id)
        scenes.clear()

        assert loaded_scenes == ["InitialScene", "Scene"]


class TestMemorySceneStorageSave:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id):

        storage = MemorySceneStorage()
        scenes = ["InitialScene", "Scene"]

        await storage.save(scenes, chat_id=chat_id, user_id=user_id)

        assert await storage.load(chat_id=chat_id, user_id=user_id) == scenes

    @pytest.mark.asyncio
    async def test_mutability(self, chat_id, user_id):

        storage = MemorySceneStorage()
        scenes = ["InitialScene", "Scene"]

        await storage.save(scenes, chat_id=chat_id, user_id=user_id)
        scenes.clear()

        assert await storage.load(chat_id=chat_id, user_id=user_id) == ["InitialScene", "Scene"]
