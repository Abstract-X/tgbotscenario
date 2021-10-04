from tgbotscenario.asynchronous import BaseScene, MemorySceneStorage
from tgbotscenario.asynchronous.scenes.manager import SceneManager


def test():

    class InitialScene(BaseScene):
        pass

    initial_scene = InitialScene()
    manager = SceneManager(initial_scene, MemorySceneStorage())

    assert manager.scenes == {initial_scene}
