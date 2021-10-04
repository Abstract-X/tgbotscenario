import pytest

from tgbotscenario.asynchronous import BaseScene, MemorySceneStorage
from tgbotscenario.asynchronous.scenes.manager import SceneManager
from tgbotscenario import errors


def test_scene_exists():

    class InitialScene(BaseScene):
        pass

    class SomeScene(BaseScene):
        pass

    some_scene = SomeScene()
    manager = SceneManager(InitialScene(), MemorySceneStorage())
    manager.add_scene(some_scene)

    scene = manager.get_scene("SomeScene")

    assert scene is some_scene


def test_scene_not_exists():

    class InitialScene(BaseScene):
        pass

    manager = SceneManager(InitialScene(), MemorySceneStorage())

    with pytest.raises(errors.SceneNotFoundError):
        manager.get_scene("SomeScene")
