import pytest

from tgbotscenario.asynchronous import Machine, Scene, MemorySceneStorage
from tgbotscenario import errors


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("test_direction",)
    )
)
def test_behavior(direction, trigger):
    foo_scene = Scene("FooScene")
    bar_scene = Scene("BarScene")
    machine = Machine(Scene("InitialScene"), MemorySceneStorage())

    machine.add_transition(foo_scene, bar_scene, trigger, direction)

    assert machine.check_transition(foo_scene, bar_scene, trigger, direction)
    assert foo_scene in machine.scenes
    assert bar_scene in machine.scenes


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("test_direction",)
    )
)
def test_duplicate_scene_name(direction, trigger):
    foo_scene = Scene("FooScene")
    another_foo_scene = Scene("FooScene")
    machine = Machine(Scene("InitialScene"), MemorySceneStorage())

    with pytest.raises(errors.DuplicateSceneNameError):
        machine.add_transition(foo_scene, another_foo_scene, trigger, direction)


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("test_direction",)
    )
)
def test_transition_exists(direction, trigger):
    machine = Machine(Scene("InitialScene"), MemorySceneStorage())
    foo_scene = Scene("FooScene")
    bar_scene = Scene("BarScene")
    machine.add_transition(foo_scene, bar_scene, trigger, direction)

    with pytest.raises(errors.TransitionExistsError):
        machine.add_transition(foo_scene, bar_scene, trigger, direction)


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("test_direction",)
    )
)
def test_transition_busy(direction, trigger):
    machine = Machine(Scene("InitialScene"), MemorySceneStorage())
    foo_scene = Scene("FooScene")
    bar_scene = Scene("BarScene")
    baz_scene = Scene("BazScene")
    machine.add_transition(foo_scene, bar_scene, trigger, direction)

    with pytest.raises(errors.TransitionBusyError):
        machine.add_transition(foo_scene, baz_scene, trigger, direction)
