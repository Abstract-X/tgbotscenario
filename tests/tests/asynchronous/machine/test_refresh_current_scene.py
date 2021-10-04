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
async def test(chat_id, user_id, scene_mock_factory, event, handler_data):

    class Scene(BaseScene):
        pass

    scene_mock = scene_mock_factory(Scene())
    machine = Machine(scene_mock, MemorySceneStorage())

    await machine.refresh_current_scene(event, handler_data, chat_id=chat_id, user_id=user_id)

    current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
    assert current_scene is scene_mock
    scene_mock.process_enter.assert_awaited_once_with(event, handler_data)
    scene_mock.process_exit.assert_not_awaited()


@pytest.mark.asyncio
async def test_unknown_scene_in_storage(chat_id, user_id, event):

    class InitialScene(BaseScene):
        pass

    storage = MemorySceneStorage()
    await storage.save_scenes(["InitialScene", "UnknownScene"], chat_id=chat_id, user_id=user_id)
    machine = Machine(InitialScene(), storage)

    with pytest.raises(errors.UnknownSceneError):
        await machine.refresh_current_scene(event, chat_id=chat_id, user_id=user_id)
