import asyncio

import pytest

from tgbotscenario.asynchronous.machines.context import ContextMachine
from tgbotscenario.asynchronous.machines.scenario import ScenarioMachine
from tgbotscenario.asynchronous.scenes.storages.memory import MemorySceneStorage
from tgbotscenario.asynchronous.scenes.scene import BaseScene
from tgbotscenario import errors
import tgbotscenario.errors.scenario_machine


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("direction",)
    )
)
class TestContextMachineMoveToNextScene:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, context_data, scene_mock_factory, event, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene_mock = scene_mock_factory(InitialScene())
        scene_mock = scene_mock_factory(Scene())
        machine = ScenarioMachine(initial_scene_mock, MemorySceneStorage())
        machine.add_transition(initial_scene_mock, scene_mock, handler, direction)
        context_machine = ContextMachine(machine, context_data)

        await context_machine.move_to_next_scene(direction)

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is scene_mock
        initial_scene_mock.process_exit.assert_awaited_once_with(event)
        scene_mock.process_enter.assert_awaited_once_with(event)

    @pytest.mark.asyncio
    async def test_transition_not_exists(self, chat_id, user_id, context_data, direction):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemorySceneStorage())
        context_machine = ContextMachine(machine, context_data)

        with pytest.raises(errors.scenario_machine.NextTransitionNotFoundError):
            await context_machine.move_to_next_scene(direction)

    @pytest.mark.asyncio
    async def test_concurrent_transitions(self, chat_id, user_id, context_data,
                                          scene_mock_factory, event, handler, direction):

        class InitialScene(BaseScene):
            async def process_exit(self, _) -> None:
                await asyncio.sleep(0.05)

        class Scene(BaseScene):
            async def process_enter(self, _) -> None:
                await asyncio.sleep(0.05)

        initial_scene_mock = scene_mock_factory(InitialScene())
        scene_mock = scene_mock_factory(Scene())
        machine = ScenarioMachine(initial_scene_mock, MemorySceneStorage())
        machine.add_transition(initial_scene_mock, scene_mock, handler, direction)
        context_machine = ContextMachine(machine, context_data)

        first_task = asyncio.create_task(
            context_machine.move_to_next_scene(direction)
        )
        await asyncio.sleep(0)  # to start the first task before the second

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            await context_machine.move_to_next_scene(direction)
        await first_task

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is scene_mock
        initial_scene_mock.process_exit.assert_awaited_once_with(event)
        scene_mock.process_enter.assert_awaited_once_with(event)

    @pytest.mark.asyncio
    async def test_same_source_and_destination_scenes(self, chat_id, user_id, context_data, scene_mock_factory,
                                                      scene_storage_mock_factory, event, handler, direction):

        class InitialScene(BaseScene):
            pass

        initial_scene_mock = scene_mock_factory(InitialScene())
        scene_storage_mock = scene_storage_mock_factory(MemorySceneStorage())
        machine = ScenarioMachine(initial_scene_mock, scene_storage_mock)
        machine.add_transition(initial_scene_mock, initial_scene_mock, handler, direction)
        context_machine = ContextMachine(machine, context_data)

        await context_machine.move_to_next_scene(direction)

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is initial_scene_mock
        scene_storage_mock.save.assert_not_awaited()
        initial_scene_mock.process_exit.assert_awaited_once_with(event)
        initial_scene_mock.process_enter.assert_awaited_once_with(event)


class TestContextMachineMoveToPreviousScene:

    @pytest.mark.parametrize(
        ("direction",),
        (
            (None,),
            ("direction",)
        )
    )
    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, context_data, scene_mock_factory, event, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene_mock = scene_mock_factory(InitialScene())
        scene_mock = scene_mock_factory(Scene())
        machine = ScenarioMachine(initial_scene_mock, MemorySceneStorage())
        machine.add_transition(initial_scene_mock, scene_mock, handler, direction)
        await machine.execute_next_transition(event, handler, direction, chat_id=chat_id, user_id=user_id)
        context_machine = ContextMachine(machine, context_data)

        await context_machine.move_to_previous_scene()

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is initial_scene_mock
        scene_mock.process_exit.assert_awaited_once_with(event)
        initial_scene_mock.process_enter.assert_awaited_once_with(event)

    @pytest.mark.asyncio
    async def test_transition_not_exists(self, chat_id, user_id, context_data, event):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemorySceneStorage())
        context_machine = ContextMachine(machine, context_data)

        with pytest.raises(errors.scenario_machine.BackTransitionNotFoundError):
            await context_machine.move_to_previous_scene()

    @pytest.mark.parametrize(
        ("direction",),
        (
            (None,),
            ("direction",)
        )
    )
    @pytest.mark.asyncio
    async def test_concurrent_transitions(self, chat_id, user_id, context_data, scene_mock_factory,
                                          event, handler, direction):

        class InitialScene(BaseScene):
            async def process_enter(self, _) -> None:
                await asyncio.sleep(0.05)

        class Scene(BaseScene):
            async def process_exit(self, _) -> None:
                await asyncio.sleep(0.05)

        initial_scene_mock = scene_mock_factory(InitialScene())
        scene_mock = scene_mock_factory(Scene())
        machine = ScenarioMachine(initial_scene_mock, MemorySceneStorage())
        machine.add_transition(initial_scene_mock, scene_mock, handler, direction)
        await machine.execute_next_transition(event, handler, direction, chat_id=chat_id, user_id=user_id)
        context_machine = ContextMachine(machine, context_data)

        first_task = asyncio.create_task(
            context_machine.move_to_previous_scene()
        )
        await asyncio.sleep(0)  # to start the first task before the second

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            await context_machine.move_to_previous_scene()
        await first_task

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is initial_scene_mock
        scene_mock.process_exit.assert_awaited_once_with(event)
        initial_scene_mock.process_enter.assert_awaited_once_with(event)


class TestContextMachineRefreshScene:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, context_data, scene_mock_factory, event):

        class InitialScene(BaseScene):
            pass

        initial_scene_mock = scene_mock_factory(InitialScene())
        machine = ScenarioMachine(initial_scene_mock, MemorySceneStorage())
        context_machine = ContextMachine(machine, context_data)

        await context_machine.refresh_scene()

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is initial_scene_mock
        initial_scene_mock.process_enter.assert_awaited_once_with(event)
        initial_scene_mock.process_exit.assert_not_awaited()
