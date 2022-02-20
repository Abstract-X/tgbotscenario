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
def test_behavior(direction):
    async def foo_to_bar_trigger():
        pass

    async def bar_to_baz_trigger():
        pass

    foo_scene = Scene("FooScene")
    bar_scene = Scene("BarScene")
    baz_scene = Scene("BazScene")
    machine = Machine(Scene("InitialScene"), MemorySceneStorage())
    machine.add_transition(foo_scene, bar_scene, foo_to_bar_trigger, direction)
    machine.add_transition(bar_scene, baz_scene, bar_to_baz_trigger)

    destination_scene = machine.remove_transition(foo_scene, foo_to_bar_trigger, direction)

    assert not machine.check_transition(foo_scene, bar_scene, foo_to_bar_trigger, direction)
    assert destination_scene is bar_scene
    assert foo_scene not in machine.scenes
    assert bar_scene in machine.scenes


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("test_direction",)
    )
)
def test_transition_for_removing_not_exists(direction, trigger):
    foo_scene = Scene("FooScene")
    machine = Machine(Scene("InitialScene"), MemorySceneStorage())

    with pytest.raises(errors.TransitionForRemovingNotFoundError):
        machine.remove_transition(foo_scene, trigger, direction)
