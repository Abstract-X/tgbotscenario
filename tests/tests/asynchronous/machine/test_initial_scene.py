from tgbotscenario.asynchronous import Machine, BaseScene, MemorySceneStorage


def test():

    class InitialScene(BaseScene):
        pass

    initial_scene = InitialScene()
    machine = Machine(initial_scene, MemorySceneStorage())

    assert machine.initial_scene is initial_scene
