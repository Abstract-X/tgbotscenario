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
def test(direction, handler):

    class SourceScene(BaseScene):
        pass

    class DestinationScene(BaseScene):
        pass

    source_scene = SourceScene()
    destination_scene = DestinationScene()
    scheme = TransitionScheme()

    scheme.add_transition(source_scene, destination_scene, handler, direction)

    assert scheme.check_transition(source_scene, destination_scene, handler, direction)


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        (generate_direction(),)
    )
)
def test_transition_exists(direction, handler):

    class SourceScene(BaseScene):
        pass

    class DestinationScene(BaseScene):
        pass

    source_scene = SourceScene()
    destination_scene = DestinationScene()
    scheme = TransitionScheme()
    scheme.add_transition(source_scene, destination_scene, handler, direction)

    with pytest.raises(errors.TransitionExistsError):
        scheme.add_transition(source_scene, destination_scene, handler, direction)


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        (generate_direction(),)
    )
)
def test_transition_busy(direction, handler):

    class SourceScene(BaseScene):
        pass

    class DestinationScene(BaseScene):
        pass

    class AnotherDestinationScene(BaseScene):
        pass

    source_scene = SourceScene()
    destination_scene = DestinationScene()
    another_destination_scene = AnotherDestinationScene()
    scheme = TransitionScheme()
    scheme.add_transition(source_scene, destination_scene, handler, direction)

    with pytest.raises(errors.TransitionBusyError):
        scheme.add_transition(source_scene, another_destination_scene, handler, direction)
