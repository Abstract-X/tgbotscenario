from tgbotscenario.asynchronous import Machine, Scene, MemorySceneStorage


def test_behavior():
    initial_scene = Scene("InitialScene")
    machine = Machine(initial_scene, MemorySceneStorage())

    assert machine.initial_scene is initial_scene
