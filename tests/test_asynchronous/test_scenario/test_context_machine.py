from unittest.mock import AsyncMock
import asyncio

import pytest

from tgbotscenario.asynchronous.scenario.machine import ScenarioMachine
from tgbotscenario.asynchronous.scenario.context_machine import ContextMachine
from tgbotscenario.asynchronous.scenario.scene import BaseScene
from tgbotscenario.asynchronous.states.storages.memory import MemoryStateStorage
from tgbotscenario import errors
import tgbotscenario.errors.scenario_machine


class TestContextMachineMoveToNextScene:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene_mock = AsyncMock(InitialScene)
        foo_scene_mock = AsyncMock(FooScene)
        foo_scene_mock.name = "FooScene"
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        await context_machine.move_to_next_scene()
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        foo_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    @pytest.mark.asyncio
    async def test_transition_not_exists(self, context_data):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        context_machine = ContextMachine(machine, context_data)

        with pytest.raises(errors.scenario_machine.NextTransitionNotFoundError):
            await context_machine.move_to_next_scene()

    @pytest.mark.asyncio
    async def test_concurrent_transitions(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        async def fake_process(event):
            await asyncio.sleep(0.1)

        initial_scene_mock = AsyncMock(InitialScene)
        initial_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock = AsyncMock(FooScene)
        foo_scene_mock.name = "FooScene"
        foo_scene_mock.process_enter.side_effect = fake_process
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        first_task = asyncio.create_task(
            machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        )
        await asyncio.sleep(0)  # to start the first task before the second

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            await context_machine.move_to_next_scene()

        await first_task
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        foo_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    @pytest.mark.asyncio
    async def test_suppress_lock_error(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        async def fake_process(event):
            await asyncio.sleep(0.1)

        initial_scene_mock = AsyncMock(InitialScene)
        initial_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock = AsyncMock(FooScene)
        foo_scene_mock.name = "FooScene"
        foo_scene_mock.process_enter.side_effect = fake_process
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage(), suppress_lock_error=True)
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        await asyncio.gather(
            machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub),
            context_machine.move_to_next_scene()
        )
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        foo_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"


class TestContextMachineMoveToPreviousScene:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene_mock = AsyncMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        foo_scene_mock = AsyncMock(FooScene)
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        await context_machine.move_to_previous_scene()
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        initial_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"

    @pytest.mark.asyncio
    async def test_previous_state_not_exists(self, context_data):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        context_machine = ContextMachine(machine, context_data)

        with pytest.raises(errors.scenario_machine.BackTransitionNotFoundError):
            await context_machine.move_to_previous_scene()

    @pytest.mark.asyncio
    async def test_concurrent_transitions(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        async def fake_process(event):
            await asyncio.sleep(0.1)

        initial_scene_mock = AsyncMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        initial_scene_mock.process_enter.side_effect = fake_process
        foo_scene_mock = AsyncMock(FooScene)
        foo_scene_mock.process_exit.side_effect = fake_process

        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        first_task = asyncio.create_task(
            machine.execute_back_transition(event_stub, chat_id=chat_id, user_id=user_id)
        )
        await asyncio.sleep(0)  # to start the first task before the second

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            await context_machine.move_to_previous_scene()

        await first_task
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        initial_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"

    @pytest.mark.asyncio
    async def test_suppress_lock_error(self, chat_id, user_id, context_data, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        # noinspection PyUnusedLocal
        async def fake_process(event):
            await asyncio.sleep(0.1)

        initial_scene_mock = AsyncMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        initial_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock = AsyncMock(FooScene)
        foo_scene_mock.process_exit.side_effect = fake_process
        foo_scene_mock.process_enter.side_effect = fake_process
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage(), suppress_lock_error=True)
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        context_machine = ContextMachine(machine, context_data)
        await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        await asyncio.gather(
            machine.execute_back_transition(event_stub, chat_id=chat_id, user_id=user_id),
            context_machine.move_to_previous_scene()
        )
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        initial_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"


class TestContextMachineRefreshScene:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, event_stub, context_data):

        class InitialScene(BaseScene):
            pass

        initial_scene_mock = AsyncMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        context_machine = ContextMachine(machine, context_data)
        await context_machine.refresh_scene()
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        initial_scene_mock.process_exit.assert_not_awaited()
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"
