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

    class SourceScene(BaseScene):
        pass

    class Scene(BaseScene):
        pass

    source_scene_mock = scene_mock_factory(SourceScene())
    scene_mock = scene_mock_factory(Scene())
    machine = Machine(source_scene_mock, MemorySceneStorage())
    machine.add_transition(source_scene_mock, scene_mock, handler)

    await machine.set_current_scene(scene_mock, event, handler_data, chat_id=chat_id, user_id=user_id)

    current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
    assert current_scene is scene_mock
    scene_mock.process_enter.assert_awaited_once_with(event, handler_data)
    source_scene_mock.process_exit.assert_not_awaited()


@pytest.mark.asyncio
async def test_scene_not_in_transition_scenes(chat_id, user_id, event):

    class InitialScene(BaseScene):
        pass

    class Scene(BaseScene):
        pass

    machine = Machine(InitialScene(), MemorySceneStorage())

    with pytest.raises(errors.SceneSetError):
        await machine.set_current_scene(Scene(), event, chat_id=chat_id, user_id=user_id)


@pytest.mark.asyncio
async def test_unknown_scene_in_storage(chat_id, user_id, event, handler):

    class SourceScene(BaseScene):
        pass

    class Scene(BaseScene):
        pass

    storage = MemorySceneStorage()
    source_scene = SourceScene()
    scene = Scene()
    await storage.save_scenes(["InitialScene", "UnknownScene"], chat_id=chat_id, user_id=user_id)
    machine = Machine(source_scene, storage)
    machine.add_transition(source_scene, scene, handler)

    with pytest.raises(errors.UnknownSceneError):
        await machine.set_current_scene(scene, event, chat_id=chat_id, user_id=user_id)


@pytest.mark.asyncio
async def test_transition_in_progress(chat_id, user_id, event, handler):

    class SourceScene(BaseScene):
        async def process_exit(self, event, data) -> None:
            await asyncio.sleep(0.05)

    class DestinationScene(BaseScene):
        pass

    class Scene(BaseScene):
        pass

    source_scene = SourceScene()
    destination_scene = DestinationScene()
    machine = Machine(source_scene, MemorySceneStorage())
    machine.add_transition(source_scene, destination_scene, handler)
    task = asyncio.create_task(machine.execute_next_transition(event, handler, chat_id=chat_id, user_id=user_id))
    await asyncio.sleep(0)

    with pytest.raises(errors.SceneSetError):
        await machine.set_current_scene(Scene(), event, chat_id=chat_id, user_id=user_id)
    await task
