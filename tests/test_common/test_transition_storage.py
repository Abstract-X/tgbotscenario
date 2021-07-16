import pytest

from tgbotscenario.common.transition_storage import TransitionStorage
from tgbotscenario.asynchronous.scenario.scene import BaseScene
from tgbotscenario import errors
import tgbotscenario.errors.transition_storage


class TestTransitionStorageScenes:

    def test_transitions_not_added(self):

        storage = TransitionStorage()

        assert storage.scenes == set()

    def test_transitions_added(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler)

        assert storage.scenes == {initial_scene, foo_scene}


class TestTransitionStorageAdd:

    def test_without_direction(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler)

        assert storage.check(initial_scene, foo_scene, handler)
        assert initial_scene in storage.scenes
        assert foo_scene in storage.scenes

    def test_with_direction(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler, "some_direction")

        assert storage.check(initial_scene, foo_scene, handler, "some_direction")
        assert initial_scene in storage.scenes
        assert foo_scene in storage.scenes

    def test_transition_exists(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler)

        with pytest.raises(errors.transition_storage.TransitionExistsError):
            storage.add(initial_scene, foo_scene, handler)

    def test_transition_busy(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        class BarScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        bar_scene = BarScene()
        storage.add(initial_scene, foo_scene, handler)

        with pytest.raises(errors.transition_storage.TransitionBusyError):
            storage.add(initial_scene, bar_scene, handler)


class TestTransitionStorageCheck:

    def test(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler)

        assert storage.check(initial_scene, foo_scene, handler) is True

        storage.remove(initial_scene, handler)

        assert storage.check(initial_scene, foo_scene, handler) is False


class TestTransitionStorageRemove:

    def test(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler)
        destination_scene = storage.remove(initial_scene, handler)

        assert not storage.check(initial_scene, foo_scene, handler)
        assert destination_scene is foo_scene
        assert initial_scene not in storage.scenes
        assert foo_scene not in storage.scenes

    def test_transition_not_exists(self, handler):

        class InitialScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()

        with pytest.raises(errors.transition_storage.TransitionForRemovingNotFoundError):
            storage.remove(initial_scene, handler)


class TestTransitionStorageGetDestinationScene:

    def test(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler)
        destination_scene = storage.get_destination_scene(initial_scene, handler)

        assert destination_scene is foo_scene

    def test_transition_not_exists(self, handler):

        class InitialScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()

        with pytest.raises(errors.transition_storage.DestinationSceneNotFoundError):
            storage.get_destination_scene(initial_scene, handler)
