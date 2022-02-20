from tgbotscenario.asynchronous import Machine, Scene, MemorySceneStorage


def test_transitions_not_exists():
    initial_scene = Scene("InitialScene")
    machine = Machine(initial_scene, MemorySceneStorage())

    assert machine.scenes == {initial_scene}


def test_transitions_exists():
    async def initial_to_foo_trigger():
        pass

    async def foo_to_bar_trigger():
        pass

    initial_scene = Scene("InitialScene")
    foo_scene = Scene("FooScene")
    bar_scene = Scene("BarScene")
    machine = Machine(initial_scene, MemorySceneStorage())
    machine.add_transition(initial_scene, foo_scene, initial_to_foo_trigger)
    machine.add_transition(foo_scene, bar_scene, foo_to_bar_trigger)

    assert machine.scenes == {initial_scene, foo_scene, bar_scene}


def test_immutability():
    initial_scene = Scene("InitialScene")
    machine = Machine(initial_scene, MemorySceneStorage())

    machine.scenes.clear()

    assert machine.scenes == {initial_scene}
