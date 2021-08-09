from unittest.mock import AsyncMock
import asyncio

import pytest

from tgbotscenario.asynchronous.scenario.machine import ScenarioMachine
from tgbotscenario.asynchronous.scenario.scene import BaseScene
from tgbotscenario.asynchronous.states.storages.memory import MemoryStateStorage
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

    def test_with_transition(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler_stub)

        assert machine.scenes == {initial_scene, foo_scene}


class TestScenarioMachineGetCurrentScene:

    @pytest.mark.asyncio
    async def test_initialized_machine(self, chat_id, user_id):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)

        assert current_scene is initial_scene

    @pytest.mark.asyncio
    async def test_after_transition(self, chat_id, user_id, handler_stub, event_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler_stub)
        await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)

        assert current_scene is foo_scene

    @pytest.mark.asyncio
    async def test_scene_not_exists(self, chat_id, user_id, event_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        await machine.migrate_to_scene(foo_scene, event_stub, chat_id=chat_id, user_id=user_id)

        with pytest.raises(errors.scenario_machine.CurrentSceneNotFoundError):
            await machine.get_current_scene(chat_id=chat_id, user_id=user_id)


class TestScenarioMachineGetCurrentState:

    @pytest.mark.asyncio
    async def test_initialized_machine(self, chat_id, user_id):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        assert current_state == "InitialScene"

    @pytest.mark.asyncio
    async def test_after_transition(self, chat_id, user_id, handler_stub, event_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler_stub)
        await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        assert current_state == "FooScene"


class TestScenarioMachineAddTransition:

    def test_without_direction(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler_stub)

        assert machine.check_transition(initial_scene, foo_scene, handler_stub)
        assert initial_scene in machine.scenes
        assert foo_scene in machine.scenes

    def test_with_direction(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler_stub, "some_direction")

        assert machine.check_transition(initial_scene, foo_scene, handler_stub, "some_direction")
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

        async def initial_handler():
            pass

        async def foo_bar_handler():
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

    def test_without_direction(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler_stub)

        assert machine.check_transition(initial_scene, foo_scene, handler_stub) is True

        machine.remove_transition(initial_scene, handler_stub)

        assert machine.check_transition(initial_scene, foo_scene, handler_stub) is False

    def test_with_direction(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler_stub, "some_direction")

        assert machine.check_transition(initial_scene, foo_scene, handler_stub, "some_direction") is True

        machine.remove_transition(initial_scene, handler_stub, "some_direction")

        assert machine.check_transition(initial_scene, foo_scene, handler_stub) is False


class TestScenarioMachineRemoveTransition:

    def test_without_direction(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler_stub)
        destination_scene = machine.remove_transition(initial_scene, handler_stub)

        assert not machine.check_transition(initial_scene, foo_scene, handler_stub)
        assert destination_scene is foo_scene
        assert initial_scene in machine.scenes
        assert foo_scene not in machine.scenes

    def test_with_direction(self, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())
        machine.add_transition(initial_scene, foo_scene, handler_stub, "some_direction")
        destination_scene = machine.remove_transition(initial_scene, handler_stub, "some_direction")

        assert not machine.check_transition(initial_scene, foo_scene, handler_stub, "some_direction")
        assert destination_scene is foo_scene
        assert initial_scene in machine.scenes
        assert foo_scene not in machine.scenes


class TestScenarioMachineMigrateToScene:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene_mock = AsyncMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        foo_scene_mock = AsyncMock(FooScene)
        foo_scene_mock.name = "FooScene"
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        await machine.migrate_to_scene(foo_scene_mock, event_stub, chat_id=chat_id, user_id=user_id)
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_not_awaited()
        foo_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"


class TestRefreshCurrentScene:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, event_stub):

        class InitialScene(BaseScene):
            pass

        initial_scene_mock = AsyncMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        await machine.refresh_current_scene(event_stub, chat_id=chat_id, user_id=user_id)
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        initial_scene_mock.process_exit.assert_not_awaited()
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"


class TestScenarioMachineExecuteNextTransition:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene_mock = AsyncMock(InitialScene)
        foo_scene_mock = AsyncMock(FooScene)
        foo_scene_mock.name = "FooScene"
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        foo_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    @pytest.mark.asyncio
    async def test_transition_not_exists(self, chat_id, user_id, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())

        with pytest.raises(errors.scenario_machine.NextTransitionNotFoundError):
            await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)

    @pytest.mark.asyncio
    async def test_concurrent_transitions(self, chat_id, user_id, event_stub, handler_stub):

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
        first_task = asyncio.create_task(
            machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        )
        await asyncio.sleep(0)  # to start the first task before the second

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)

        await first_task
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        foo_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    @pytest.mark.asyncio
    async def test_suppress_lock_error(self, chat_id, user_id, event_stub, handler_stub):

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
        await asyncio.gather(
            *[machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
              for _ in range(2)]
        )
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        initial_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        foo_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is foo_scene_mock
        assert current_state == "FooScene"

    @pytest.mark.asyncio
    async def test_same_source_and_destination_scenes(self, chat_id, user_id, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        initial_scene_mock = AsyncMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        storage = MemoryStateStorage()
        storage_mock = AsyncMock(storage)
        storage_mock.load.side_effect = storage.load
        storage_mock.save.side_effect = storage.save
        machine = ScenarioMachine(initial_scene_mock, storage_mock)
        machine.add_transition(initial_scene_mock, initial_scene_mock, handler_stub)
        await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        storage_mock.save.assert_not_awaited()
        initial_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        initial_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"


class TestScenarioMachineExecuteBackTransition:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, event_stub, handler_stub):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene_mock = AsyncMock(InitialScene)
        initial_scene_mock.name = "InitialScene"
        foo_scene_mock = AsyncMock(FooScene)
        machine = ScenarioMachine(initial_scene_mock, MemoryStateStorage())
        machine.add_transition(initial_scene_mock, foo_scene_mock, handler_stub)
        await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        await machine.execute_back_transition(event_stub, chat_id=chat_id, user_id=user_id)

        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        initial_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"

    @pytest.mark.asyncio
    async def test_previous_state_not_exists(self, chat_id, user_id, event_stub):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemoryStateStorage())

        with pytest.raises(errors.scenario_machine.BackTransitionNotFoundError):
            await machine.execute_back_transition(event_stub, chat_id=chat_id, user_id=user_id)

    @pytest.mark.asyncio
    async def test_concurrent_transitions(self, chat_id, user_id, event_stub, handler_stub):

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
        await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        first_task = asyncio.create_task(
            machine.execute_back_transition(event_stub, chat_id=chat_id, user_id=user_id)
        )
        await asyncio.sleep(0)  # to start the first task before the second

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            await machine.execute_back_transition(event_stub, chat_id=chat_id, user_id=user_id)

        await first_task
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        initial_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"

    @pytest.mark.asyncio
    async def test_suppress_lock_error(self, chat_id, user_id, event_stub, handler_stub):

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
        await machine.execute_next_transition(event_stub, chat_id=chat_id, user_id=user_id, handler=handler_stub)
        await asyncio.gather(
            *[machine.execute_back_transition(event_stub, chat_id=chat_id, user_id=user_id)
              for _ in range(2)]
        )
        current_scene = await machine.get_current_scene(chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        foo_scene_mock.process_exit.assert_awaited_once_with(event_stub)
        initial_scene_mock.process_enter.assert_awaited_once_with(event_stub)
        assert current_scene is initial_scene_mock
        assert current_state == "InitialScene"
