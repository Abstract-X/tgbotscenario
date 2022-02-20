import pytest

from tgbotscenario.asynchronous import MemorySceneStorage


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (-100123456789, 123456789),
        (123456789, 123456789)
    )
)
async def test_scenes_not_exists(chat_id, user_id):
    storage = MemorySceneStorage()

    assert await storage.load_scenes(chat_id=chat_id, user_id=user_id) == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (-100123456789, 123456789),
        (123456789, 123456789)
    )
)
@pytest.mark.parametrize(
    ("scenes",),
    (
        (["InitialScene"],),
        (["InitialScene", "FooScene"],)
    )
)
async def test_scenes_exists(chat_id, user_id, scenes):
    storage = MemorySceneStorage()
    await storage.save_scenes(scenes, chat_id=chat_id, user_id=user_id)

    assert await storage.load_scenes(chat_id=chat_id, user_id=user_id) == scenes


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (-100123456789, 123456789),
        (123456789, 123456789)
    )
)
@pytest.mark.parametrize(
    ("scenes",),
    (
        (["InitialScene"],),
        (["InitialScene", "FooScene"],)
    )
)
async def test_immutability(chat_id, user_id, scenes):
    storage = MemorySceneStorage()
    saving_scenes = scenes.copy()
    await storage.save_scenes(saving_scenes, chat_id=chat_id, user_id=user_id)

    loaded_scenes = await storage.load_scenes(chat_id=chat_id, user_id=user_id)
    saving_scenes.clear()

    assert loaded_scenes == scenes
