import pytest

from tgbotscenario.asynchronous import Machine, BaseScene, MemorySceneStorage
from tgbotscenario import errors
from tests.generators import generate_chat_id


@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (generate_chat_id(), generate_chat_id()),  # different
        (generate_chat_id(),) * 2  # same
    )
)
@pytest.mark.asyncio
async def test_initial_scene(chat_id, user_id):

    class InitialScene(BaseScene):
        pass

    initial_scene = InitialScene()
    machine = Machine(initial_scene, MemorySceneStorage())

    current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)

    assert current_scene is initial_scene


@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (generate_chat_id(), generate_chat_id()),  # different
        (generate_chat_id(),) * 2  # same
    )
)
@pytest.mark.asyncio
async def test_transition_executed(chat_id, user_id, handler, event):

    class SourceScene(BaseScene):
        pass

    class DestinationScene(BaseScene):
        pass

    source_scene = SourceScene()
    destination_scene = DestinationScene()
    machine = Machine(source_scene, MemorySceneStorage())
    machine.add_transition(source_scene, destination_scene, handler)
    await machine.execute_next_transition(event, handler, chat_id=chat_id, user_id=user_id)

    current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)

    assert current_scene is destination_scene


@pytest.mark.asyncio
async def test_unknown_scene_in_storage(chat_id, user_id):

    class InitialScene(BaseScene):
        pass

    storage = MemorySceneStorage()
    await storage.save_scenes(["InitialScene", "UnknownScene"], chat_id=chat_id, user_id=user_id)
    machine = Machine(InitialScene(), storage)

    with pytest.raises(errors.UnknownSceneError):
        await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
