import asyncio

import pytest

from tgbotscenario.asynchronous import Machine, ContextMachine, BaseScene, MemorySceneStorage
from tgbotscenario.common import ContextData
from tgbotscenario import errors
from tests.contexts import Context, chat_id_context, user_id_context, event_context, handler_context
from tests.generators import generate_direction, generate_handler_data, generate_chat_id


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        (generate_direction(),)
    )
)
@pytest.mark.parametrize(
    ("handler_data",),
    (
        (None,),
        (generate_handler_data(),)
    )
)
@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (generate_chat_id(), generate_chat_id()),  # different
        (generate_chat_id(),) * 2  # same
    )
)
@pytest.mark.asyncio
async def test(chat_id, user_id, handler_data, direction, handler, event, scene_mock_factory):

    class SourceScene(BaseScene):
        pass

    class DestinationScene(BaseScene):
        pass

    source_scene_mock = scene_mock_factory(SourceScene())
    destination_scene_mock = scene_mock_factory(DestinationScene())
    machine = Machine(source_scene_mock, MemorySceneStorage())
    machine.add_transition(source_scene_mock, destination_scene_mock, handler, direction)
    context_data = ContextData(chat_id=chat_id_context, user_id=user_id_context,
                               handler=handler_context, event=event_context)
    context_machine = ContextMachine(machine, context_data)
    with Context(chat_id, user_id, handler, event):

        await context_machine.execute_next_transition(direction, handler_data)

    current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
    assert current_scene is destination_scene_mock
    source_scene_mock.process_exit.assert_awaited_once_with(event, handler_data)
    destination_scene_mock.process_enter.assert_awaited_once_with(event, handler_data)


@pytest.mark.asyncio
async def test_unknown_scene_in_storage(chat_id, user_id, event, handler):

    class InitialScene(BaseScene):
        pass

    storage = MemorySceneStorage()
    await storage.save_scenes(["InitialScene", "UnknownScene"], chat_id=chat_id, user_id=user_id)
    machine = Machine(InitialScene(), storage)
    context_data = ContextData(chat_id=chat_id_context, user_id=user_id_context,
                               handler=handler_context, event=event_context)
    context_machine = ContextMachine(machine, context_data)
    with Context(chat_id, user_id, handler, event):

        with pytest.raises(errors.UnknownSceneError):
            await context_machine.execute_next_transition()


@pytest.mark.asyncio
async def test_transition_not_found(chat_id, user_id, event, handler):

    class SourceScene(BaseScene):
        pass

    machine = Machine(SourceScene(), MemorySceneStorage())
    context_data = ContextData(chat_id=chat_id_context, user_id=user_id_context,
                               handler=handler_context, event=event_context)
    context_machine = ContextMachine(machine, context_data)
    with Context(chat_id, user_id, handler, event):

        with pytest.raises(errors.NextTransitionNotFoundError):
            await context_machine.execute_next_transition()


@pytest.mark.asyncio
async def test_double_transition(chat_id, user_id, scene_mock_factory, event, handler):

    class SourceScene(BaseScene):
        async def process_exit(self, event, data) -> None:
            await asyncio.sleep(0.05)

    class DestinationScene(BaseScene):
        async def process_enter(self, event, data) -> None:
            await asyncio.sleep(0.05)

    source_scene_mock = scene_mock_factory(SourceScene())
    destination_scene_mock = scene_mock_factory(DestinationScene())
    machine = Machine(source_scene_mock, MemorySceneStorage())
    machine.add_transition(source_scene_mock, destination_scene_mock, handler)
    context_data = ContextData(chat_id=chat_id_context, user_id=user_id_context,
                               handler=handler_context, event=event_context)
    context_machine = ContextMachine(machine, context_data)
    with Context(chat_id, user_id, handler, event):
        first_task = asyncio.create_task(context_machine.execute_next_transition())
        await asyncio.sleep(0)

        with pytest.raises(errors.DoubleTransitionError):
            await context_machine.execute_next_transition()
        await first_task
    current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
    assert current_scene is destination_scene_mock
    source_scene_mock.process_exit.assert_awaited_once_with(event, None)
    destination_scene_mock.process_enter.assert_awaited_once_with(event, None)
