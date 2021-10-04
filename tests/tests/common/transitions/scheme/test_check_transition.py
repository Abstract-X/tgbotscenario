import pytest

from tgbotscenario.common.transitions.scheme import TransitionScheme
from tgbotscenario.common.scene import BaseScene
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
    scheme = TransitionScheme()

    assert scheme.check_transition(initial_scene, scene, handler, direction) is False


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
    scheme = TransitionScheme()
    scheme.add_transition(initial_scene, scene, handler, direction)

    assert scheme.check_transition(initial_scene, scene, handler, direction) is True
