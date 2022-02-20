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
@pytest.mark.parametrize(
    ("data",),
    (
        (None,),
        ({"test_key": "test_value"},)
    )
)
async def test_behavior(chat_id, user_id, data, scene_mock_factory, event):
    scene = scene_mock_factory(Scene("InitialScene"))
    machine = Machine(scene, MemorySceneStorage())

    await machine.reset_current_scene(event, data, chat_id=chat_id, user_id=user_id)

    assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is scene
    scene.process_enter.assert_awaited_once_with(event, data)
    scene.process_exit.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (-100123456789, 123456789),
        (123456789, 123456789)
    )
)
@pytest.mark.parametrize(
    ("data",),
    (
        (None,),
        ({"test_key": "test_value"},)
    )
)
async def test_unknown_scene_in_storage(chat_id, user_id, data, event):
    storage = MemorySceneStorage()
    await storage.save_scenes(["InitialScene", "UnknownScene"], chat_id=chat_id, user_id=user_id)
    machine = Machine(Scene("InitialScene"), storage)

    with pytest.raises(errors.UnknownSceneError):
        await machine.reset_current_scene(event, data, chat_id=chat_id, user_id=user_id)
