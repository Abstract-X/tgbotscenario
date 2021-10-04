import pytest

from tgbotscenario.asynchronous import BaseScene, MemorySceneStorage
from tgbotscenario.asynchronous.scenes.manager import SceneManager
from tgbotscenario import errors


def test():

    class InitialScene(BaseScene):
        pass

    class SomeScene(BaseScene):
        pass

    some_scene = SomeScene()
    manager = SceneManager(InitialScene(), MemorySceneStorage())

    manager.add_scene(some_scene)

    scene = manager.get_scene("SomeScene")
    assert scene is some_scene
    assert some_scene in manager.scenes


def test_duplicate_scene_name():

    class InitialScene(BaseScene):
        pass

    class FooScene(BaseScene):
        pass

    class BarScene(BaseScene):
        pass

    foo_scene = FooScene()
    bar_scene = BarScene("FooScene")
    manager = SceneManager(InitialScene(), MemorySceneStorage())
    manager.add_scene(foo_scene)

    with pytest.raises(errors.DuplicateSceneNameError):
        manager.add_scene(bar_scene)
