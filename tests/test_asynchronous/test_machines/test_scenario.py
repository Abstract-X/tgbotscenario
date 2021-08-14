import asyncio

import pytest

from tgbotscenario.asynchronous.machines.scenario import ScenarioMachine
from tgbotscenario.asynchronous.scenes.base import BaseScene
from tgbotscenario.asynchronous.scenes.storages.memory import MemorySceneStorage
from tgbotscenario import errors
import tgbotscenario.errors.scenario_machine


class TestScenarioMachineInitialScene:

    def test(self):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemorySceneStorage())

        assert machine.initial_scene is initial_scene


class TestScenarioMachineScenes:

    def test(self):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemorySceneStorage())

        assert machine.scenes == frozenset({initial_scene})


class TestScenarioMachineGetCurrentScene:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemorySceneStorage())

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is initial_scene

    @pytest.mark.parametrize(
        ("direction",),
        (
            (None,),
            ("direction",)
        )
    )
    @pytest.mark.asyncio
    async def test_after_transition(self, chat_id, user_id, event, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        machine = ScenarioMachine(initial_scene, MemorySceneStorage())
        machine.add_transition(initial_scene, scene, handler, direction)
        await machine.execute_next_transition(event, handler, direction, chat_id=chat_id, user_id=user_id)

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is scene


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("direction",)
    )
)
class TestScenarioMachineAddTransition:

    def test(self, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        machine = ScenarioMachine(initial_scene, MemorySceneStorage())

        machine.add_transition(initial_scene, scene, handler, direction)

        assert machine.check_transition(initial_scene, scene, handler, direction)
        assert initial_scene in machine.scenes
        assert scene in machine.scenes


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("direction",)
    )
)
class TestScenarioMachineCheckTransition:

    def test_transition_not_exists(self, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        machine = ScenarioMachine(initial_scene, MemorySceneStorage())

        assert machine.check_transition(initial_scene, scene, handler, direction) is False

    def test_transition_exists(self, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        machine = ScenarioMachine(initial_scene, MemorySceneStorage())
        machine.add_transition(initial_scene, scene, handler, direction)

        assert machine.check_transition(initial_scene, scene, handler, direction) is True


class TestScenarioMachineMigrateToScene:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, scene_mock_factory, event):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene_mock = scene_mock_factory(InitialScene())
        scene_mock = scene_mock_factory(Scene())
        machine = ScenarioMachine(initial_scene_mock, MemorySceneStorage())

        await machine.migrate_to_scene(scene_mock, event, chat_id=chat_id, user_id=user_id)

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is scene_mock
        assert initial_scene_mock in machine.scenes
        assert scene_mock in machine.scenes
        scene_mock.process_enter.assert_awaited_once_with(event)
        initial_scene_mock.process_exit.assert_not_awaited()


class TestScenarioMachineRefreshCurrentScene:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, scene_mock_factory, event):

        class InitialScene(BaseScene):
            pass

        initial_scene_mock = scene_mock_factory(InitialScene())
        machine = ScenarioMachine(initial_scene_mock, MemorySceneStorage())

        await machine.refresh_current_scene(event, chat_id=chat_id, user_id=user_id)

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is initial_scene_mock
        initial_scene_mock.process_enter.assert_awaited_once_with(event)
        initial_scene_mock.process_exit.assert_not_awaited()


@pytest.mark.parametrize(
    ("direction",),
    (
        (None,),
        ("direction",)
    )
)
class TestScenarioMachineExecuteNextTransition:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, scene_mock_factory, event, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene_mock = scene_mock_factory(InitialScene())
        scene_mock = scene_mock_factory(Scene())
        machine = ScenarioMachine(initial_scene_mock, MemorySceneStorage())
        machine.add_transition(initial_scene_mock, scene_mock, handler, direction)

        await machine.execute_next_transition(event, handler, direction, chat_id=chat_id, user_id=user_id)

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is scene_mock
        initial_scene_mock.process_exit.assert_awaited_once_with(event)
        scene_mock.process_enter.assert_awaited_once_with(event)

    @pytest.mark.asyncio
    async def test_transition_not_exists(self, chat_id, user_id, event, handler, direction):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemorySceneStorage())

        with pytest.raises(errors.scenario_machine.NextTransitionNotFoundError):
            await machine.execute_next_transition(event, handler, direction, chat_id=chat_id, user_id=user_id)

    @pytest.mark.asyncio
    async def test_concurrent_transitions(self, chat_id, user_id, scene_mock_factory, event, handler, direction):

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

        first_task = asyncio.create_task(
            machine.execute_next_transition(event, handler, direction, chat_id=chat_id, user_id=user_id)
        )
        await asyncio.sleep(0)  # to start the first task before the second

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            await machine.execute_next_transition(event, handler, direction, chat_id=chat_id, user_id=user_id)
        await first_task

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is scene_mock
        initial_scene_mock.process_exit.assert_awaited_once_with(event)
        scene_mock.process_enter.assert_awaited_once_with(event)

    @pytest.mark.asyncio
    async def test_same_source_and_destination_scenes(self, chat_id, user_id, scene_mock_factory,
                                                      scene_storage_mock_factory, event, handler, direction):

        class InitialScene(BaseScene):
            pass

        initial_scene_mock = scene_mock_factory(InitialScene())
        scene_storage_mock = scene_storage_mock_factory(MemorySceneStorage())
        machine = ScenarioMachine(initial_scene_mock, scene_storage_mock)
        machine.add_transition(initial_scene_mock, initial_scene_mock, handler, direction)

        await machine.execute_next_transition(event, handler, direction, chat_id=chat_id, user_id=user_id)

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is initial_scene_mock
        scene_storage_mock.save.assert_not_awaited()
        initial_scene_mock.process_exit.assert_awaited_once_with(event)
        initial_scene_mock.process_enter.assert_awaited_once_with(event)


class TestScenarioMachineExecuteBackTransition:

    @pytest.mark.parametrize(
        ("direction",),
        (
            (None,),
            ("direction",)
        )
    )
    @pytest.mark.asyncio
    async def test(self, chat_id, user_id, scene_mock_factory, event, handler, direction):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene_mock = scene_mock_factory(InitialScene())
        scene_mock = scene_mock_factory(Scene())
        machine = ScenarioMachine(initial_scene_mock, MemorySceneStorage())
        machine.add_transition(initial_scene_mock, scene_mock, handler, direction)
        await machine.execute_next_transition(event, handler, direction, chat_id=chat_id, user_id=user_id)

        await machine.execute_back_transition(event, chat_id=chat_id, user_id=user_id)

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is initial_scene_mock
        scene_mock.process_exit.assert_awaited_once_with(event)
        initial_scene_mock.process_enter.assert_awaited_once_with(event)

    @pytest.mark.asyncio
    async def test_transition_not_exists(self, chat_id, user_id, event):

        class InitialScene(BaseScene):
            pass

        initial_scene = InitialScene()
        machine = ScenarioMachine(initial_scene, MemorySceneStorage())

        with pytest.raises(errors.scenario_machine.BackTransitionNotFoundError):
            await machine.execute_back_transition(event, chat_id=chat_id, user_id=user_id)

    @pytest.mark.parametrize(
        ("direction",),
        (
            (None,),
            ("direction",)
        )
    )
    @pytest.mark.asyncio
    async def test_concurrent_transitions(self, chat_id, user_id, scene_mock_factory, event, handler, direction):

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

        first_task = asyncio.create_task(
            machine.execute_back_transition(event, chat_id=chat_id, user_id=user_id)
        )
        await asyncio.sleep(0)  # to start the first task before the second

        with pytest.raises(errors.scenario_machine.TransitionLockedError):
            await machine.execute_back_transition(event, chat_id=chat_id, user_id=user_id)
        await first_task

        assert await machine.get_current_scene(chat_id=chat_id, user_id=user_id) is initial_scene_mock
        scene_mock.process_exit.assert_awaited_once_with(event)
        initial_scene_mock.process_enter.assert_awaited_once_with(event)
