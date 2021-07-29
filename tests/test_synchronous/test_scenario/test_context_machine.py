from contextvars import ContextVar
from unittest.mock import MagicMock
from threading import Thread
import time

import pytest

from tgbotscenario.synchronous.scenario.machine import ScenarioMachine
from tgbotscenario.synchronous.scenario.context_machine import ContextMachine, ContextData
from tgbotscenario.synchronous.scenario.scene import BaseScene
from tgbotscenario.synchronous.states.storages.memory import MemoryStateStorage
from tgbotscenario import errors
import tgbotscenario.errors.scenario_machine


chat_id_context = ContextVar("chat_id_context")
user_id_context = ContextVar("user_id_context")
handler_context = ContextVar("handler_context")
event_context = ContextVar("event_context")


@pytest.fixture()
def context_data(chat_id, user_id, handler, telegram_event_stub):

    data = ContextData(chat_id=chat_id_context, user_id=user_id_context, handler=handler_context, event=event_context)

    chat_id_token = chat_id_context.set(chat_id)
    user_id_token = user_id_context.set(user_id)
    handler_token = handler_context.set(handler)
    event_token = event_context.set(telegram_event_stub)

    yield data

    chat_id_context.reset(chat_id_token)
    user_id_context.reset(user_id_token)
    handler_context.reset(handler_token)
    event_context.reset(event_token)


class TestContextMachineMoveToNextScene:

    def test(self, chat_id, user_id, context_data, telegram_event_stub, scene_data_stub, handler):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene_mock = MagicMock(InitialScene)
        foo_scene_mock = MagicMock(FooScene)
        foo_scene_mock.name = "FooScene"
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler)
        context_machine = ContextMachine(machine, context_data, scene_data_stub)
        context_machine.move_to_next_scene()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        foo_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    def test_transition_not_exists(self, context_data, scene_data_stub):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        context_machine = ContextMachine(machine, context_data, scene_data_stub)

        with pytest.raises(errors.scenario_machine.NextTransitionNotFoundError):
            context_machine.move_to_next_scene()

    def test_concurrent_transitions(self, chat_id, user_id, context_data, telegram_event_stub,
                                    scene_data_stub, handler):

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
        context_machine = ContextMachine(machine, context_data, scene_data_stub)
        thread = Thread(target=machine.execute_next_transition, kwargs={
            "chat_id": chat_id,
            "user_id": user_id,
            "scene_args": (telegram_event_stub, scene_data_stub),
            "handler": handler
        })
        thread.start()

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            context_machine.move_to_next_scene()

        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        foo_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    def test_suppress_lock_error(self, chat_id, user_id, context_data, telegram_event_stub,
                                 scene_data_stub, handler):

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
        context_machine = ContextMachine(machine, context_data, scene_data_stub)
        thread = Thread(target=machine.execute_next_transition, kwargs={
            "chat_id": chat_id,
            "user_id": user_id,
            "scene_args": (telegram_event_stub, scene_data_stub),
            "handler": handler
        })
        thread.start()
        context_machine.move_to_next_scene()
        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        foo_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"


class TestContextMachineMoveToPreviousScene:

    def test(self, chat_id, user_id, context_data, telegram_event_stub, handler, scene_data_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        foo_scene_mock = MagicMock(FooScene)
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler)
        context_machine = ContextMachine(machine, context_data, scene_data_stub)
        machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub), handler=handler)
        context_machine.move_to_previous_scene()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        initial_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"

    def test_previous_state_not_exists(self, scene_data_stub, context_data):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        context_machine = ContextMachine(machine, context_data, scene_data_stub)

        with pytest.raises(errors.scenario_machine.BackTransitionNotFoundError):
            context_machine.move_to_previous_scene()

    def test_concurrent_transitions(self, chat_id, user_id, context_data, telegram_event_stub,
                                    scene_data_stub, handler):

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
        context_machine = ContextMachine(machine, context_data, scene_data_stub)
        machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub), handler=handler)
        thread = Thread(target=machine.execute_back_transition, kwargs={
            "chat_id": chat_id,
            "user_id": user_id,
            "scene_args": (telegram_event_stub, scene_data_stub)
        })
        thread.start()

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            context_machine.move_to_previous_scene()

        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        initial_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"

    def test_suppress_lock_error(self, chat_id, user_id, context_data, telegram_event_stub,
                                 scene_data_stub, handler):

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
        context_machine = ContextMachine(machine, context_data, scene_data_stub)
        machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                        scene_args=(telegram_event_stub, scene_data_stub), handler=handler)
        thread = Thread(target=machine.execute_back_transition, kwargs={
            "chat_id": chat_id,
            "user_id": user_id,
            "scene_args": (telegram_event_stub, scene_data_stub)
        })
        thread.start()
        context_machine.move_to_previous_scene()
        thread.join()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_called_once_with(telegram_event_stub, scene_data_stub)
        initial_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"


class TestContextMachineRefreshScene:

    def test(self, chat_id, user_id, telegram_event_stub, context_data, scene_data_stub):

        class InitialScene(BaseScene):
            pass

        initial_scene_mock = MagicMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        context_machine = ContextMachine(machine, context_data, scene_data_stub)
        context_machine.refresh_scene()
        current_scene = machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_enter.assert_called_once_with(telegram_event_stub, scene_data_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"
