import pytest

from tgbotscenario.asynchronous import Machine, BaseScene, MemorySceneStorage
from tests.generators import generate_direction


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        (generate_direction(),)
    )
)
def test_transition_not_exists(direction, handler):

    class InitialScene(BaseScene):
        pass

    class Scene(BaseScene):
        pass

    initial_scene = InitialScene()
    scene = Scene()
    machine = Machine(initial_scene, MemorySceneStorage())

    assert machine.check_transition(initial_scene, scene, handler, direction) is False


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        (generate_direction(),)
    )
)
def test_transition_exists(direction, handler):

    class InitialScene(BaseScene):
        pass

    class Scene(BaseScene):
        pass

    initial_scene = InitialScene()
    scene = Scene()
    machine = Machine(initial_scene, MemorySceneStorage())
    machine.add_transition(initial_scene, scene, handler, direction)

    assert machine.check_transition(initial_scene, scene, handler, direction) is True
