import pytest

from tgbotscenario.common.transition_storage import TransitionStorage
from tgbotscenario.asynchronous.scenario.scene import BaseScene
from tgbotscenario import errors
import tgbotscenario.errors.transition_storage


class TestTransitionStorageScenes:

    def test_transitions_not_added(self):

        storage = TransitionStorage()

        assert storage.scenes == set()

    def test_transitions_added(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler_stub)

        assert storage.scenes == {initial_scene, foo_scene}


class TestTransitionStorageAdd:

    def test_without_direction(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler_stub)

        assert storage.check(initial_scene, foo_scene, handler_stub)
        assert initial_scene in storage.scenes
        assert foo_scene in storage.scenes

    def test_with_direction(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler_stub, "some_direction")

        assert storage.check(initial_scene, foo_scene, handler_stub, "some_direction")
        assert initial_scene in storage.scenes
        assert foo_scene in storage.scenes

    def test_transition_exists(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler_stub)

        with pytest.raises(errors.transition_storage.TransitionExistsError):
            storage.add(initial_scene, foo_scene, handler_stub)

    def test_transition_busy(self, handler_stub):

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
        storage.add(initial_scene, foo_scene, handler_stub)

        with pytest.raises(errors.transition_storage.TransitionBusyError):
            storage.add(initial_scene, bar_scene, handler_stub)


class TestTransitionStorageCheck:

    def test(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler_stub)

        assert storage.check(initial_scene, foo_scene, handler_stub) is True

        storage.remove(initial_scene, handler_stub)

        assert storage.check(initial_scene, foo_scene, handler_stub) is False


class TestTransitionStorageRemove:

    def test(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler_stub)
        destination_scene = storage.remove(initial_scene, handler_stub)

        assert not storage.check(initial_scene, foo_scene, handler_stub)
        assert destination_scene is foo_scene
        assert initial_scene not in storage.scenes
        assert foo_scene not in storage.scenes

    def test_transition_not_exists(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()

        with pytest.raises(errors.transition_storage.TransitionForRemovingNotFoundError):
            storage.remove(initial_scene, handler_stub)


class TestTransitionStorageGetDestinationScene:

    def test(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()
        foo_scene = FooScene()
        storage.add(initial_scene, foo_scene, handler_stub)
        destination_scene = storage.get_destination_scene(initial_scene, handler_stub)

        assert destination_scene is foo_scene

    def test_transition_not_exists(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        storage = TransitionStorage()
        initial_scene = InitialScene()

        with pytest.raises(errors.transition_storage.DestinationSceneNotFoundError):
            storage.get_destination_scene(initial_scene, handler_stub)
