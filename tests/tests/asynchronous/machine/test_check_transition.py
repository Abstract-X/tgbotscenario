import pytest

from tgbotscenario.asynchronous import Machine, Scene, MemorySceneStorage


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("test_direction",)
    )
)
def test_transition_not_exists(direction, trigger):
    foo_scene = Scene("FooScene")
    bar_scene = Scene("BarScene")
    machine = Machine(Scene("InitialScene"), MemorySceneStorage())

    assert machine.check_transition(foo_scene, bar_scene, trigger, direction) is False


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("test_direction",)
    )
)
def test_transition_exists(direction, trigger):
    foo_scene = Scene("FooScene")
    bar_scene = Scene("BarScene")
    machine = Machine(Scene("InitialScene"), MemorySceneStorage())
    machine.add_transition(foo_scene, bar_scene, trigger, direction)

    assert machine.check_transition(foo_scene, bar_scene, trigger, direction) is True
