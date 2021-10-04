import pytest

from tgbotscenario.asynchronous import Machine, ContextMachine, BaseScene, MemorySceneStorage
from tgbotscenario.common import ContextData
from tgbotscenario import errors
from tests.generators import generate_chat_id, generate_handler_data
from tests.contexts import Context, chat_id_context, user_id_context, handler_context, event_context


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
async def test(chat_id, user_id, scene_mock_factory, handler, event, handler_data):

    class Scene(BaseScene):
        pass

    scene_mock = scene_mock_factory(Scene())
    machine = Machine(scene_mock, MemorySceneStorage())
    context_data = ContextData(chat_id=chat_id_context, user_id=user_id_context,
                               handler=handler_context, event=event_context)
    context_machine = ContextMachine(machine, context_data)
    with Context(chat_id, user_id, handler, event):

        await context_machine.refresh_current_scene(handler_data)

    current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
    assert current_scene is scene_mock
    scene_mock.process_enter.assert_awaited_once_with(event, handler_data)
    scene_mock.process_exit.assert_not_awaited()


@pytest.mark.asyncio
async def test_unknown_scene_in_storage(chat_id, user_id, handler, event):

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
            await context_machine.refresh_current_scene()
