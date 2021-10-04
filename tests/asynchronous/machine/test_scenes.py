from tgbotscenario.asynchronous import Machine, BaseScene, MemorySceneStorage


def test_initial_scene():

    class InitialScene(BaseScene):
        pass

    initial_scene = InitialScene()
    machine = Machine(initial_scene, MemorySceneStorage())

    assert machine.scenes == {initial_scene}
