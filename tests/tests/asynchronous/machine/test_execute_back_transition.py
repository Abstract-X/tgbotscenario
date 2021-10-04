import asyncio

import pytest

from tgbotscenario.asynchronous import Machine, BaseScene, MemorySceneStorage
from tgbotscenario import errors
from tests.generators import generate_chat_id, generate_handler_data


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
async def test(chat_id, user_id, scene_mock_factory, event, handler, handler_data):

    class InitialScene(BaseScene):
        pass

    class Scene(BaseScene):
        pass

    initial_scene_mock = scene_mock_factory(InitialScene())
    scene_mock = scene_mock_factory(Scene())
    machine = Machine(initial_scene_mock, MemorySceneStorage())
    machine.add_transition(initial_scene_mock, scene_mock, handler)
    await machine.execute_next_transition(event, handler, data=handler_data, chat_id=chat_id, user_id=user_id)

    await machine.execute_back_transition(event, handler_data, chat_id=chat_id, user_id=user_id)

    current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
    assert current_scene is initial_scene_mock
    scene_mock.process_exit.assert_awaited_once_with(event, handler_data)
    initial_scene_mock.process_enter.assert_awaited_once_with(event, handler_data)


@pytest.mark.asyncio
async def test_unknown_scene_in_storage(chat_id, user_id, event):

    class InitialScene(BaseScene):
        pass

    storage = MemorySceneStorage()
    await storage.save_scenes(["InitialScene", "UnknownScene"], chat_id=chat_id, user_id=user_id)
    machine = Machine(InitialScene(), storage)

    with pytest.raises(errors.UnknownSceneError):
        await machine.execute_back_transition(event, chat_id=chat_id, user_id=user_id)


@pytest.mark.asyncio
async def test_transition_not_found(chat_id, user_id, event):

    class InitialScene(BaseScene):
        pass

    machine = Machine(InitialScene(), MemorySceneStorage())

    with pytest.raises(errors.BackTransitionNotFoundError):
        await machine.execute_back_transition(event, chat_id=chat_id, user_id=user_id)


@pytest.mark.asyncio
async def test_double_transition(chat_id, user_id, scene_mock_factory, event, handler):

    class InitialScene(BaseScene):
        async def process_enter(self, event, data) -> None:
            await asyncio.sleep(0.05)

    class Scene(BaseScene):
        async def process_exit(self, event, data) -> None:
            await asyncio.sleep(0.05)

    initial_scene_mock = scene_mock_factory(InitialScene())
    scene_mock = scene_mock_factory(Scene())
    machine = Machine(initial_scene_mock, MemorySceneStorage())
    machine.add_transition(initial_scene_mock, scene_mock, handler)
    await machine.execute_next_transition(event, handler, chat_id=chat_id, user_id=user_id)

    first_task = asyncio.create_task(machine.execute_back_transition(event, chat_id=chat_id, user_id=user_id))
    await asyncio.sleep(0)

    with pytest.raises(errors.DoubleTransitionError):
        await machine.execute_back_transition(event, chat_id=chat_id, user_id=user_id)
    await first_task
    current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
    assert current_scene is initial_scene_mock
    scene_mock.process_exit.assert_awaited_once_with(event, None)
    initial_scene_mock.process_enter.assert_awaited_once_with(event, None)
