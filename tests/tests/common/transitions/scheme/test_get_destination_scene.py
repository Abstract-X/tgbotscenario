import pytest

from tgbotscenario.common.transitions.scheme import TransitionScheme
from tgbotscenario.common.scene import BaseScene
from tgbotscenario import errors
from tests.generators import generate_direction


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        (generate_direction(),)
    )
)
def test_destination_scene_exists(direction, handler):

    class InitialScene(BaseScene):
        pass

    class Scene(BaseScene):
        pass

    scheme = TransitionScheme()
    initial_scene = InitialScene()
    scene = Scene()
    scheme.add_transition(initial_scene, scene, handler, direction)

    assert scheme.get_destination_scene(initial_scene, handler, direction) is scene


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        (generate_direction(),)
    )
)
def test_destination_scene_not_exists(direction, handler):

    class InitialScene(BaseScene):
        pass

    scheme = TransitionScheme()
    initial_scene = InitialScene()

    with pytest.raises(errors.DestinationSceneNotFoundError):
        assert scheme.get_destination_scene(initial_scene, handler, direction)
