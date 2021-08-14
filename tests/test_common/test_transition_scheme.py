import pytest

from tgbotscenario.common.transition_scheme import TransitionScheme
from tgbotscenario.common.scenes.base import BaseScene
from tgbotscenario import errors
import tgbotscenario.errors.transition_scheme


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("direction",)
    )
)
class TestTransitionSchemeAddTransition:

    def test(self, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        scheme = TransitionScheme()
        initial_scene = InitialScene()
        scene = Scene()

        scheme.add_transition(initial_scene, scene, handler, direction)

        assert scheme.check_transition(initial_scene, scene, handler, direction)

    def test_transition_exists(self, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        scheme = TransitionScheme()
        initial_scene = InitialScene()
        scene = Scene()
        scheme.add_transition(initial_scene, scene, handler, direction)

        with pytest.raises(errors.transition_scheme.TransitionExistsError):
            scheme.add_transition(initial_scene, scene, handler, direction)

    def test_transition_busy(self, handler, direction):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        class BarScene(BaseScene):
            pass

        scheme = TransitionScheme()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        bar_scene = BarScene()
        scheme.add_transition(initial_scene, foo_scene, handler, direction)

        with pytest.raises(errors.transition_scheme.TransitionBusyError):
            scheme.add_transition(initial_scene, bar_scene, handler, direction)


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("direction",)
    )
)
class TestTransitionSchemeCheckTransition:

    def test(self, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        scheme = TransitionScheme()
        initial_scene = InitialScene()
        scene = Scene()

        assert scheme.check_transition(initial_scene, scene, handler, direction) is False

    def test_transition_exists(self, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        scheme = TransitionScheme()
        initial_scene = InitialScene()
        scene = Scene()
        scheme.add_transition(initial_scene, scene, handler, direction)

        assert scheme.check_transition(initial_scene, scene, handler, direction) is True


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("direction",)
    )
)
class TestTransitionSchemeGetDestinationScene:

    def test(self, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        scheme = TransitionScheme()
        initial_scene = InitialScene()
        scene = Scene()
        scheme.add_transition(initial_scene, scene, handler, direction)

        assert scheme.get_destination_scene(initial_scene, handler, direction) is scene

    def test_transition_not_exists(self, handler, direction):

        class InitialScene(BaseScene):
            pass

        scheme = TransitionScheme()
        initial_scene = InitialScene()

        with pytest.raises(errors.transition_scheme.DestinationSceneNotFoundError):
            assert scheme.get_destination_scene(initial_scene, handler, direction)
