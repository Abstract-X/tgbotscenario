import pytest

from tgbotscenario.asynchronous.scenes.manager import SceneManager
from tgbotscenario.asynchronous.scenes.scene import BaseScene
from tgbotscenario.asynchronous.scenes.storages.memory import MemorySceneStorage
from tgbotscenario.common.scenes.magazine import SceneMagazine
from tgbotscenario import errors
import tgbotscenario.errors.scene_manager


class TestSceneManagerInitialScene:

    def test(self):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        manager = SceneManager(initial_scene, MemorySceneStorage())

        assert manager.initial_scene is initial_scene


class TestSceneManagerScenes:

    def test(self):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        manager = SceneManager(initial_scene, MemorySceneStorage())

        assert manager.scenes == frozenset({initial_scene})


class TestSceneManagerAddScene:

    def test(self):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        manager = SceneManager(initial_scene, MemorySceneStorage())

        manager.add_scene(scene)

        assert scene in manager.scenes


class TestSceneManagerLoadMagazine:

    @pytest.mark.asyncio
    async def test_with_empty_storage(self, chat_id, user_id):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        manager = SceneManager(initial_scene, MemorySceneStorage())

        magazine = await manager.load_magazine(chat_id=chat_id, user_id=user_id)

        assert magazine == SceneMagazine([initial_scene])

    @pytest.mark.asyncio
    async def test_with_not_empty_storage(self, chat_id, user_id):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        manager = SceneManager(initial_scene, MemorySceneStorage())
        magazine = SceneMagazine([initial_scene, scene])
        await manager.save_magazine(magazine, chat_id=chat_id, user_id=user_id)
        manager.add_scene(scene)

        assert await manager.load_magazine(chat_id=chat_id, user_id=user_id) == magazine

    @pytest.mark.asyncio
    async def test_unknown_scene(self, chat_id, user_id):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        manager = SceneManager(initial_scene, MemorySceneStorage())
        magazine = SceneMagazine([initial_scene, scene])
        await manager.save_magazine(magazine, chat_id=chat_id, user_id=user_id)

        with pytest.raises(errors.scene_manager.UnknownSceneError):
            await manager.load_magazine(chat_id=chat_id, user_id=user_id)


class TestSceneManagerSaveMagazine:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        manager = SceneManager(initial_scene, MemorySceneStorage())
        manager.add_scene(scene)
        magazine = SceneMagazine([initial_scene, scene])

        await manager.save_magazine(magazine, chat_id=chat_id, user_id=user_id)

        assert await manager.load_magazine(chat_id=chat_id, user_id=user_id) == magazine
