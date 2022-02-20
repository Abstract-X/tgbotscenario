import pytest

from tgbotscenario.asynchronous import Machine, Scene, MemorySceneStorage
from tgbotscenario import errors


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (-100123456789, 123456789),
        (123456789, 123456789)
    )
)
async def test_initial_scene(chat_id, user_id):
    initial_scene = Scene("InitialScene")
    machine = Machine(initial_scene, MemorySceneStorage())

    assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is initial_scene


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (-100123456789, 123456789),
        (123456789, 123456789)
    )
)
async def test_after_transition(chat_id, user_id, trigger, event):
    initial_scene = Scene("InitialScene")
    foo_scene = Scene("FooScene")
    machine = Machine(initial_scene, MemorySceneStorage())
    machine.add_transition(initial_scene, foo_scene, trigger)
    await machine.move_to_next_scene(event, trigger, chat_id=chat_id, user_id=user_id)

    assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is foo_scene


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (-100123456789, 123456789),
        (123456789, 123456789)
    )
)
async def test_unknown_scene_in_storage(chat_id, user_id):
    storage = MemorySceneStorage()
    await storage.save_scenes(["InitialScene", "UnknownScene"], chat_id=chat_id, user_id=user_id)
    machine = Machine(Scene("InitialScene"), storage)

    with pytest.raises(errors.UnknownSceneError):
        await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
