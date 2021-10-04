import pytest

from tgbotscenario.asynchronous import BaseScene, MemorySceneStorage
from tgbotscenario.asynchronous.scenes.manager import SceneManager
from tgbotscenario.common.magazine import Magazine
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
async def test_empty_scene_storage(chat_id, user_id):

    class InitialScene(BaseScene):
        pass

    initial_scene = InitialScene()
    manager = SceneManager(initial_scene, MemorySceneStorage())

    magazine = await manager.load_magazine(chat_id=chat_id, user_id=user_id)

    assert magazine == Magazine([initial_scene])


@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (generate_chat_id(), generate_chat_id()),  # different
        (generate_chat_id(),) * 2  # same
    )
)
@pytest.mark.asyncio
async def test_not_empty_scene_storage(chat_id, user_id):

    class InitialScene(BaseScene):
        pass

    class Scene(BaseScene):
        pass

    initial_scene = InitialScene()
    scene = Scene()
    manager = SceneManager(initial_scene, MemorySceneStorage())
    manager.add_scene(scene)
    await manager.save_magazine(Magazine([initial_scene, scene]), chat_id=chat_id, user_id=user_id)

    magazine = await manager.load_magazine(chat_id=chat_id, user_id=user_id)

    assert magazine == Magazine([initial_scene, scene])


@pytest.mark.asyncio
async def test_unknown_scene_in_storage(chat_id, user_id):

    class InitialScene(BaseScene):
        pass

    storage = MemorySceneStorage()
    await storage.save_scenes(["InitialScene", "UnknownScene"], chat_id=chat_id, user_id=user_id)
    manager = SceneManager(InitialScene(), storage)

    with pytest.raises(errors.UnknownSceneError):
        await manager.load_magazine(chat_id=chat_id, user_id=user_id)
