from unittest.mock import MagicMock
from threading import Thread
import time

import pytest

from tgbotscenario.synchronous.scenario.machine import ScenarioMachine
from tgbotscenario.synchronous.scenario.context_machine import ContextMachine
from tgbotscenario.synchronous.scenario.scene import BaseScene
from tgbotscenario.synchronous.states.storages.memory import MemoryStateStorage
from tgbotscenario import errors
import tgbotscenario.errors.scenario_machine


class TestContextMachineMoveToNextScene:

    def test(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene_mock = MagicMock(InitialScene)
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.name = "FooScene"
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        context_machine.move_to_next_scene()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_called_once_with(event_stub)
        foo_scene_mock.process_enter.assert_called_once_with(event_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    def test_transition_not_exists(self, context_data):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        context_machine = ContextMachine(machine, context_data)

        with pytest.raises(errors.scenario_machine.NextTransitionNotFoundError):
            context_machine.move_to_next_scene()

    def test_concurrent_transitions(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        def fake_process(event):
            time.sleep(0.1)

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.name = "FooScene"
        foo_scene_mock.process_enter.side_effect = fake_process

        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        thread = Thread(
            target=machine.execute_next_transition,
            args=(event_stub,),
            kwargs={
                "chat_id": chat_id,
                "user_id": user_id,
                "handler": handler_stub
            }
        )
        thread.start()

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            context_machine.move_to_next_scene()

        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_called_once_with(event_stub)
        foo_scene_mock.process_enter.assert_called_once_with(event_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    def test_suppress_lock_error(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        def fake_process(event):
            time.sleep(0.1)

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.name = "FooScene"
        foo_scene_mock.process_enter.side_effect = fake_process
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage(), suppress_lock_error=True)
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        thread = Thread(
            target=machine.execute_next_transition,
            args=(event_stub,),
            kwargs={
                "chat_id": chat_id,
                "user_id": user_id,
                "handler": handler_stub
            }
        )
        thread.start()
        context_machine.move_to_next_scene()
        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_called_once_with(event_stub)
        foo_scene_mock.process_enter.assert_called_once_with(event_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"


class TestContextMachineMoveToPreviousScene:

    def test(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        foo_scene_mock = MagicMock(FooScene)
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        context_machine.move_to_previous_scene()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_called_once_with(event_stub)
        initial_scene_mock.process_enter.assert_called_once_with(event_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"

    def test_previous_state_not_exists(self, context_data):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        context_machine = ContextMachine(machine, context_data)

        with pytest.raises(errors.scenario_machine.BackTransitionNotFoundError):
            context_machine.move_to_previous_scene()

    def test_concurrent_transitions(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        def fake_process(event):
            time.sleep(0.1)

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        initial_scene_mock.process_enter.side_effect = fake_process
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.process_exit.side_effect = fake_process

        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        thread = Thread(
            target=machine.execute_back_transition,
            args=(event_stub,),
            kwargs={
                "chat_id": chat_id,
                "user_id": user_id
            }
        )
        thread.start()

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            context_machine.move_to_previous_scene()

        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_called_once_with(event_stub)
        initial_scene_mock.process_enter.assert_called_once_with(event_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"

    def test_suppress_lock_error(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        def fake_process(event):
            time.sleep(0.1)

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        initial_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock.process_enter.side_effect = fake_process
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage(), suppress_lock_error=True)
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        thread = Thread(
            target=machine.execute_back_transition,
            args=(event_stub,),
            kwargs={
                "chat_id": chat_id,
                "user_id": user_id
            }
        )
        thread.start()
        context_machine.move_to_previous_scene()
        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_called_once_with(event_stub)
        initial_scene_mock.process_enter.assert_called_once_with(event_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"


class TestContextMachineRefreshScene:

    def test(self, chat_id, user_id, event_stub, context_data):

        class InitialScene(BaseScene):
            pass

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        context_machine = ContextMachine(machine, context_data)
        context_machine.refresh_scene()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_enter.assert_called_once_with(event_stub)
        initial_scene_mock.process_exit.assert_not_called()
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"
