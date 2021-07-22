from unittest.mock import MagicMock
import time
from threading import Thread

import pytest

from tgbotscenario.synchronous.scenario.machine import ScenarioMachine
from tgbotscenario.synchronous.scenario.scene import BaseScene
from tgbotscenario.synchronous.states.storages.memory import MemoryStateStorage
from tgbotscenario.common.scenario.scene_set import SceneSet
from tgbotscenario import errors
import tgbotscenario.errors.scenario_machine


class TestScenarioMachineInitialScene:

    def test(self):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())

        assert machine.initial_scene is initial_scene


class TestScenarioMachineScenes:

    def test_initialized_machine(self):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())

        assert machine.scenes == {initial_scene}

    def test_with_transition(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler)

        assert machine.scenes == {initial_scene, foo_scene}


class TestScenarioMachineGetCurrentScene:

    def test_initialized_machine(self, chat_id, user_id):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)

        assert current_scene is initial_scene

    def test_after_transition(self, chat_id, user_id, handler, telegram_event_stub, scene_data_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler)
        machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub), handler=handler)
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)

        assert current_scene is foo_scene

    def test_scene_not_exists(self, chat_id, user_id, telegram_event_stub, scene_data_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.migrate_to_scene(foo_scene, chat_id=chat_id, user_id=user_id,
                                 scene_args=(telegram_event_stub, scene_data_stub))

        with pytest.raises(errors.scenario_machine.CurrentSceneNotFoundError):
            machine.get_current_scene(chat_id=chat_id, user_id=user_id)


class TestScenarioMachineGetCurrentState:

    def test_initialized_machine(self, chat_id, user_id):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        assert current_state == "InitialScene"

    def test_after_transition(self, chat_id, user_id, handler, telegram_event_stub, scene_data_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler)
        machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub), handler=handler)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        assert current_state == "FooScene"


class TestScenarioMachineAddTransition:

    def test_without_direction(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler)

        assert machine.check_transition(initial_scene, foo_scene, handler)
        assert initial_scene in machine.scenes
        assert foo_scene in machine.scenes

    def test_with_direction(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler, "some_direction")

        assert machine.check_transition(initial_scene, foo_scene, handler, "some_direction")
        assert initial_scene in machine.scenes
        assert foo_scene in machine.scenes


class TestScenarioMachineAddTransitions:

    def test(self):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        class BarScene(BaseScene):
            pass

        class BazScene(BaseScene):
            pass

        def initial_handler():
            pass

        def foo_bar_handler():
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        bar_scene = BarScene()
        baz_scene = BazScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transitions({
            initial_scene: {
                initial_handler: foo_scene
            },
            SceneSet(foo_scene, bar_scene): {
                foo_bar_handler: {
                    "some_direction": baz_scene
                }
            }
        })

        assert machine.check_transition(initial_scene, foo_scene, initial_handler)
        assert machine.check_transition(foo_scene, baz_scene, foo_bar_handler, "some_direction")
        assert machine.check_transition(bar_scene, baz_scene, foo_bar_handler, "some_direction")
        for scene in (initial_scene, foo_scene, bar_scene, baz_scene):
            assert scene in machine.scenes


class TestScenarioMachineCheckTransition:

    def test_without_direction(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler)

        assert machine.check_transition(initial_scene, foo_scene, handler) is True

        machine.remove_transition(initial_scene, handler)

        assert machine.check_transition(initial_scene, foo_scene, handler) is False

    def test_with_direction(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler, "some_direction")

        assert machine.check_transition(initial_scene, foo_scene, handler, "some_direction") is True

        machine.remove_transition(initial_scene, handler, "some_direction")

        assert machine.check_transition(initial_scene, foo_scene, handler) is False


class TestScenarioMachineRemoveTransition:

    def test_without_direction(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler)
        destination_scene = machine.remove_transition(initial_scene, handler)

        assert not machine.check_transition(initial_scene, foo_scene, handler)
        assert destination_scene is foo_scene
        assert initial_scene in machine.scenes
        assert foo_scene not in machine.scenes

    def test_with_direction(self, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler, "some_direction")
        destination_scene = machine.remove_transition(initial_scene, handler, "some_direction")

        assert not machine.check_transition(initial_scene, foo_scene, handler, "some_direction")
        assert destination_scene is foo_scene
        assert initial_scene in machine.scenes
        assert foo_scene not in machine.scenes


class TestScenarioMachineMigrateToScene:

    def test(self, chat_id, user_id, telegram_event_stub, scene_data_stub, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        class BarScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.name = "FooScene"
        bar_scene = BarScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(foo_scene_mock, bar_scene, handler)
        machine.migrate_to_scene(foo_scene_mock, chat_id=chat_id, user_id=user_id,
                                 scene_args=(telegram_event_stub, scene_data_stub))
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    def test_concurrent_transitions(self, chat_id, user_id, telegram_event_stub, scene_data_stub, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        class BarScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        def fake_process(event, data):
            time.sleep(0.1)

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.name = "FooScene"
        foo_scene_mock.process_enter.side_effect = fake_process
        bar_scene_mock = MagicMock(BarScene)
        bar_scene_mock.process_enter.side_effect = fake_process

        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler)
        thread = Thread(target=machine.execute_next_transition, kwargs={
            "chat_id": chat_id,
            "user_id": user_id,
            "scene_args": (telegram_event_stub, scene_data_stub),
            "handler": handler
        })
        thread.start()

        with pytest.raises(errors.scenario_machine.MigrationToSceneError):
            machine.migrate_to_scene(bar_scene_mock, chat_id=chat_id, user_id=user_id,
                                     scene_args=(telegram_event_stub, scene_data_stub))

        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        foo_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"


class TestScenarioMachineExecuteNextTransition:

    def test(self, chat_id, user_id, telegram_event_stub, handler, scene_data_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene_mock = MagicMock(InitialScene)
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.name = "FooScene"
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler)
        machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub), handler=handler)
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        foo_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    def test_transition_not_exists(self, chat_id, user_id, telegram_event_stub, scene_data_stub, handler):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())

        with pytest.raises(errors.scenario_machine.NextTransitionNotFoundError):
            machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                            scene_args=(telegram_event_stub, scene_data_stub), handler=handler)

    def test_concurrent_transitions(self, chat_id, user_id, telegram_event_stub, scene_data_stub, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        def fake_process(event, data):
            time.sleep(0.1)

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.name = "FooScene"
        foo_scene_mock.process_enter.side_effect = fake_process

        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler)
        thread = Thread(target=machine.execute_next_transition, kwargs={
            "chat_id": chat_id,
            "user_id": user_id,
            "scene_args": (telegram_event_stub, scene_data_stub),
            "handler": handler
        })
        thread.start()

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            machine.execute_next_transition(
                chat_id=chat_id, user_id=user_id,
                scene_args=(telegram_event_stub, scene_data_stub), handler=handler
            )

        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        foo_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    def test_suppress_lock_error(self, chat_id, user_id, telegram_event_stub, scene_data_stub, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        def fake_process(event, data):
            time.sleep(0.1)

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.name = "FooScene"
        foo_scene_mock.process_enter.side_effect = fake_process
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage(), suppress_lock_error=True)
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler)
        thread = Thread(target=machine.execute_next_transition, kwargs={
            "chat_id": chat_id,
            "user_id": user_id,
            "scene_args": (telegram_event_stub, scene_data_stub),
            "handler": handler
        })
        thread.start()
        machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub), handler=handler)
        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        foo_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    def test_same_source_and_destination_scenes(self, chat_id, user_id, telegram_event_stub,
                                                handler, scene_data_stub):

        class InitialScene(BaseScene):
            pass

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        storage = MemoryStateStorage()
        storage_mock = MagicMock(storage)
        storage_mock.load.side_effect = storage.load
        storage_mock.save.side_effect = storage.save
        machine = ScenarioMachine(initial_scene_mock, storage_mock)
        machine.add_transition(initial_scene_mock, initial_scene_mock, handler)
        machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub), handler=handler)
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        storage_mock.save.assert_not_called()
        initial_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        initial_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"


class TestScenarioMachineExecuteBackTransition:

    def test(self, chat_id, user_id, telegram_event_stub, handler, scene_data_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        foo_scene_mock = MagicMock(FooScene)
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler)
        machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub), handler=handler)
        machine.execute_back_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub))

        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        initial_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"

    def test_previous_state_not_exists(self, chat_id, user_id, telegram_event_stub, scene_data_stub):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())

        with pytest.raises(errors.scenario_machine.BackTransitionNotFoundError):
            machine.execute_back_transition(chat_id=chat_id, user_id=user_id,
                                            scene_args=(telegram_event_stub, scene_data_stub))

    def test_concurrent_transitions(self, chat_id, user_id, telegram_event_stub, scene_data_stub, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        def fake_process(event, data):
            time.sleep(0.1)

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        initial_scene_mock.process_enter.side_effect = fake_process
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.process_exit.side_effect = fake_process

        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler)
        machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub), handler=handler)
        thread = Thread(target=machine.execute_back_transition, kwargs={
            "chat_id": chat_id,
            "user_id": user_id,
            "scene_args": (telegram_event_stub, scene_data_stub)
        })
        thread.start()

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            machine.execute_back_transition(chat_id=chat_id, user_id=user_id,
                                            scene_args=(telegram_event_stub, scene_data_stub))

        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        initial_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"

    def test_suppress_lock_error(self, chat_id, user_id, telegram_event_stub, scene_data_stub, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        def fake_process(event, data):
            time.sleep(0.1)

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        initial_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock.process_enter.side_effect = fake_process
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage(), suppress_lock_error=True)
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler)
        machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub), handler=handler)
        thread = Thread(target=machine.execute_back_transition, kwargs={
            "chat_id": chat_id,
            "user_id": user_id,
            "scene_args": (telegram_event_stub, scene_data_stub)
        })
        thread.start()
        machine.execute_back_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub))
        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        initial_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"
