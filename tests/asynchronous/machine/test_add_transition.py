import pytest

from tgbotscenario.asynchronous import Machine, BaseScene, MemorySceneStorage
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
    machine = Machine(source_scene, MemorySceneStorage())

    machine.add_transition(source_scene, destination_scene, handler, direction)

    assert machine.check_transition(source_scene, destination_scene, handler, direction)
    assert source_scene in machine.scenes
    assert destination_scene in machine.scenes


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        (generate_direction(),)
    )
)
def test_transition_exists(handler, direction):

    class SourceScene(BaseScene):
        pass

    class DestinationScene(BaseScene):
        pass

    source_scene = SourceScene()
    destination_scene = DestinationScene()
    machine = Machine(source_scene, MemorySceneStorage())
    machine.add_transition(source_scene, destination_scene, handler, direction)

    with pytest.raises(errors.TransitionExistsError):
        machine.add_transition(source_scene, destination_scene, handler, direction)


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        (generate_direction(),)
    )
)
def test_transition_busy(handler, direction):

    class SourceScene(BaseScene):
        pass

    class DestinationScene(BaseScene):
        pass

    class AnotherDestinationScene(BaseScene):
        pass

    source_scene = SourceScene()
    destination_scene = DestinationScene()
    another_destination_scene = AnotherDestinationScene()
    machine = Machine(source_scene, MemorySceneStorage())
    machine.add_transition(source_scene, destination_scene, handler, direction)

    with pytest.raises(errors.TransitionBusyError):
        machine.add_transition(source_scene, another_destination_scene, handler, direction)


def test_duplicate_scene_name(handler):

    class SourceScene(BaseScene):
        pass

    class DestinationScene(BaseScene):
        pass

    source_scene = SourceScene(name="TestName")
    destination_scene = DestinationScene(name="TestName")
    machine = Machine(source_scene, MemorySceneStorage())

    with pytest.raises(errors.DuplicateSceneNameError):
        machine.add_transition(source_scene, destination_scene, handler)
