import asyncio

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
async def test_behavior(chat_id, user_id, data, trigger, event, scene_mock_factory):
    initial_scene = scene_mock_factory(Scene("InitialScene"))
    foo_scene = scene_mock_factory(Scene("FooScene"))
    machine = Machine(initial_scene, MemorySceneStorage())
    machine.add_transition(initial_scene, foo_scene, trigger)

    await machine.set_current_scene(foo_scene, event, data, chat_id=chat_id, user_id=user_id)

    assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is foo_scene
    foo_scene.process_enter.assert_awaited_once_with(event, data)
    initial_scene.process_exit.assert_not_awaited()


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
async def test_scene_does_not_participate_in_transitions(chat_id, user_id, data, event):
    machine = Machine(Scene("InitialScene"), MemorySceneStorage())

    with pytest.raises(errors.SceneSettingError):
        await machine.set_current_scene(Scene("FooScene"), event, data,
                                        chat_id=chat_id, user_id=user_id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (-100123456789, 123456789),
        (123456789, 123456789)
    )
)
async def test_transition_in_progress(chat_id, user_id, event):
    class InitialScene(Scene):
        async def process_exit(self, event, data) -> None:
            await asyncio.sleep(0.05)

    async def initial_to_foo_trigger():
        pass

    async def foo_to_bar_trigger():
        pass

    initial_scene = InitialScene()
    foo_scene = Scene("FooScene")
    bar_scene = Scene("BarScene")
    machine = Machine(initial_scene, MemorySceneStorage())
    machine.add_transition(initial_scene, foo_scene, initial_to_foo_trigger)
    machine.add_transition(foo_scene, bar_scene, foo_to_bar_trigger)
    task = asyncio.create_task(machine.move_to_next_scene(event, initial_to_foo_trigger,
                                                          chat_id=chat_id, user_id=user_id))
    await asyncio.sleep(0)

    with pytest.raises(errors.SceneSettingError):
        await machine.set_current_scene(bar_scene, event, chat_id=chat_id, user_id=user_id)
    await task


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (-100123456789, 123456789),
        (123456789, 123456789)
    )
)
async def test_unknown_scene_in_storage(chat_id, user_id, trigger, event):
    storage = MemorySceneStorage()
    await storage.save_scenes(["InitialScene", "UnknownScene"], chat_id=chat_id, user_id=user_id)
    initial_scene = Scene("InitialScene")
    foo_scene = Scene("FooScene")
    machine = Machine(initial_scene, storage)
    machine.add_transition(initial_scene, foo_scene, trigger)

    with pytest.raises(errors.UnknownSceneError):
        await machine.set_current_scene(foo_scene, event, chat_id=chat_id, user_id=user_id)
