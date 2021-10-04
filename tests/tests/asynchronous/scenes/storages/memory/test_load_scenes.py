import pytest

from tgbotscenario.asynchronous import MemorySceneStorage
from tests.generators import generate_chat_id


@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (generate_chat_id(), generate_chat_id()),  # different
        (generate_chat_id(),) * 2  # same
    )
)
@pytest.mark.asyncio
async def test_scenes_not_exists(chat_id, user_id):

    storage = MemorySceneStorage()

    scenes = await storage.load_scenes(chat_id=chat_id, user_id=user_id)

    assert scenes == []


@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (generate_chat_id(), generate_chat_id()),  # different
        (generate_chat_id(),) * 2  # same
    )
)
@pytest.mark.asyncio
async def test_scenes_exists(chat_id, user_id):

    storage = MemorySceneStorage()
    await storage.save_scenes(["InitialScene", "Scene"], chat_id=chat_id, user_id=user_id)

    scenes = await storage.load_scenes(chat_id=chat_id, user_id=user_id)

    assert scenes == ["InitialScene", "Scene"]


@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (generate_chat_id(), generate_chat_id()),  # different
        (generate_chat_id(),) * 2  # same
    )
)
@pytest.mark.asyncio
async def test_mutability(chat_id, user_id):

    storage = MemorySceneStorage()
    source_scenes = ["InitialScene", "Scene"]
    await storage.save_scenes(source_scenes, chat_id=chat_id, user_id=user_id)

    scenes = await storage.load_scenes(chat_id=chat_id, user_id=user_id)
    source_scenes.clear()

    assert scenes == ["InitialScene", "Scene"]
