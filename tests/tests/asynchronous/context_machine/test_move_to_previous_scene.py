import asyncio

import pytest

from tgbotscenario.asynchronous import Machine, ContextMachine, Scene, MemorySceneStorage
from tgbotscenario.common import Context
from tgbotscenario import errors
from tests.context import (ContextVarsContext, chat_id_context, user_id_context,
                           trigger_context, event_context)


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
async def test_behavior(chat_id, user_id, data, event, scene_mock_factory, trigger):
    initial_scene = scene_mock_factory(Scene("InitialScene"))
    foo_scene = scene_mock_factory(Scene("FooScene"))
    machine = Machine(initial_scene, MemorySceneStorage())
    machine.add_transition(initial_scene, foo_scene, trigger)
    context = Context(chat_id_context, user_id_context, trigger_context, event_context)
    context_machine = ContextMachine(machine, context)
    await machine.move_to_next_scene(event, trigger, chat_id=chat_id, user_id=user_id)

    with ContextVarsContext(chat_id, user_id, trigger, event):
        await context_machine.move_to_previous_scene(data)

    assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is initial_scene
    foo_scene.process_exit.assert_awaited_once_with(event, data)
    initial_scene.process_enter.assert_awaited_once_with(event, data)


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
async def test_unknown_scene_in_storage(chat_id, user_id, data, event, trigger):
    storage = MemorySceneStorage()
    await storage.save_scenes(["InitialScene", "UnknownScene"], chat_id=chat_id, user_id=user_id)
    machine = Machine(Scene("InitialScene"), storage)
    context = Context(chat_id_context, user_id_context, trigger_context, event_context)
    context_machine = ContextMachine(machine, context)

    with ContextVarsContext(chat_id, user_id, trigger, event):
        with pytest.raises(errors.UnknownSceneError):
            await context_machine.move_to_previous_scene(data)


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
async def test_move_from_initial_scene(chat_id, user_id, data, event, trigger):
    machine = Machine(Scene("InitialScene"), MemorySceneStorage())
    context = Context(chat_id_context, user_id_context, trigger_context, event_context)
    context_machine = ContextMachine(machine, context)

    with ContextVarsContext(chat_id, user_id, trigger, event):
        with pytest.raises(errors.TransitionToPreviousSceneError):
            await context_machine.move_to_previous_scene(data)


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
async def test_double_transition(chat_id, user_id, data, event, trigger, scene_mock_factory):
    class InitialScene(Scene):
        async def process_enter(self, event, data) -> None:
            await asyncio.sleep(0.05)

    class FooScene(Scene):
        async def process_exit(self, event, data) -> None:
            await asyncio.sleep(0.05)

    initial_scene = scene_mock_factory(InitialScene())
    foo_scene = scene_mock_factory(FooScene())
    machine = Machine(initial_scene, MemorySceneStorage())
    machine.add_transition(initial_scene, foo_scene, trigger)
    context = Context(chat_id_context, user_id_context, trigger_context, event_context)
    context_machine = ContextMachine(machine, context)
    await machine.move_to_next_scene(event, trigger, chat_id=chat_id, user_id=user_id)

    task = asyncio.create_task(machine.move_to_previous_scene(event, data,
                                                              chat_id=chat_id, user_id=user_id))
    await asyncio.sleep(0)

    with ContextVarsContext(chat_id, user_id, trigger, event):
        with pytest.raises(errors.DoubleTransitionError):
            await context_machine.move_to_previous_scene(data)
    await task
    foo_scene.process_exit.assert_awaited_once_with(event, data)
    initial_scene.process_enter.assert_awaited_once_with(event, data)
