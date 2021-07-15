from typing import Optional, Callable, Set, Tuple, Any

from tgbotscenario.asynchronous.scenario.scene import BaseScene
from tgbotscenario.asynchronous.scenario.locks.base import AbstractLockStorage
from tgbotscenario.asynchronous.scenario.locks.memory import MemoryLockStorage
from tgbotscenario.asynchronous.states.machine import StateMachine
from tgbotscenario.asynchronous.states.storages.base import AbstractStateStorage
from tgbotscenario.common.scenario.mapping import SceneMapping
from tgbotscenario.common.scenario.scene_set import SceneSet
from tgbotscenario.common.states.magazine import StateMagazine
from tgbotscenario.common.transition_storage import TransitionStorage
from tgbotscenario.types import TransitionDict
from tgbotscenario import errors
import tgbotscenario.errors.scenario_machine
import tgbotscenario.errors.lock_storage
import tgbotscenario.errors.transition_storage
import tgbotscenario.errors.scene_mapping


class ScenarioMachine:

    def __init__(self, initial_scene: BaseScene, state_storage: AbstractStateStorage, *,
                 lock_storage: Optional[AbstractLockStorage] = None, suppress_lock_error: bool = False):

        self._initial_scene = initial_scene
        self._state_machine = StateMachine(initial_scene.name, state_storage)
        self._scene_mapping = SceneMapping((initial_scene,))
        self._transition_storage = TransitionStorage()
        self._lock_storage = lock_storage or MemoryLockStorage()
        self._suppress_lock_error = suppress_lock_error

    @property
    def initial_scene(self) -> Optional[BaseScene]:

        return self._initial_scene

    @property
    def scenes(self) -> Set[BaseScene]:

        return self._scene_mapping.scenes

    async def get_current_scene(self, *, chat_id: int, user_id: int) -> BaseScene:

        current_state = await self._state_machine.get_current_state(chat_id=chat_id, user_id=user_id)
        try:
            scene = self._scene_mapping.get(current_state)
        except errors.scene_mapping.SceneNameNotFoundError:
            raise errors.scenario_machine.CurrentSceneNotFoundError(
                "current scene not found (state={state!r}), because it is not involved in transitions!",
                chat_id=chat_id, user_id=user_id, state=current_state
            ) from None

        return scene

    async def get_current_state(self, *, chat_id: int, user_id: int) -> str:

        return await self._state_machine.get_current_state(chat_id=chat_id, user_id=user_id)

    def add_transition(self, source_scene: BaseScene, destination_scene: BaseScene,
                       handler: Callable, direction: Optional[str] = None) -> None:

        self._transition_storage.add(source_scene, destination_scene, handler, direction)
        for scene in (source_scene, destination_scene):
            self._scene_mapping.add(scene)

    def add_transitions(self, transitions: TransitionDict) -> None:

        for source_scenes_key in transitions:
            source_scenes = (
                SceneSet(source_scenes_key) if isinstance(source_scenes_key, BaseScene) else source_scenes_key
            )
            for source_scene in source_scenes:
                for handler in transitions[source_scenes_key]:
                    item = transitions[source_scenes_key][handler]
                    if isinstance(item, BaseScene):
                        items = ((None, item),)  # None-direction and destination scene
                    elif isinstance(item, dict):
                        items = item.items()  # directions and destination scenes
                    else:
                        raise TypeError(f"unknown direction type {type(item).__name__!r}!")

                    for direction, destination_scene in items:
                        self.add_transition(source_scene, destination_scene, handler, direction)

    def check_transition(self, source_scene: BaseScene, destination_scene: BaseScene,
                         handler: Callable, direction: Optional[str] = None) -> bool:

        return self._transition_storage.check(source_scene, destination_scene, handler, direction)

    def remove_transition(self, source_scene: BaseScene, handler: Callable,
                          direction: Optional[str] = None) -> BaseScene:

        destination_scene = self._transition_storage.remove(source_scene, handler, direction)
        if (destination_scene is not self.initial_scene) and (destination_scene not in self._transition_storage.scenes):
            self._scene_mapping.remove(destination_scene.name)

        return destination_scene

    async def migrate_to_scene(self, scene: BaseScene, *, chat_id: int,
                               user_id: int, scene_args: Tuple[Any, Any]) -> None:

        try:
            async with self._lock_storage.acquire(chat_id=chat_id, user_id=user_id):
                magazine = await self._state_machine.load_magazine(chat_id=chat_id, user_id=user_id)
                await scene.process_enter(*scene_args)
                await self._save_state_with_magazine(scene.name, magazine, chat_id=chat_id, user_id=user_id)
        except errors.lock_storage.TransitionLockExistsError:
            raise errors.scenario_machine.MigrationToSceneError(
                "there was an error migrating to the scene {scene!r} because a transition lock "
                "is active (chat_id={chat_id!r}, user_id={user_id!r})!",
                chat_id=chat_id, user_id=user_id, scene=scene
            ) from None

    async def execute_next_transition(self, *, chat_id: int, user_id: int, scene_args: Tuple[Any, Any],
                                      handler: Callable, direction: Optional[str] = None) -> None:

        try:
            async with self._lock_storage.acquire(chat_id=chat_id, user_id=user_id):
                magazine = await self._state_machine.load_magazine(chat_id=chat_id, user_id=user_id)
                source_scene = self._scene_mapping.get(magazine.current)
                try:
                    destination_scene = self._transition_storage.get_destination_scene(source_scene, handler, direction)
                except errors.transition_storage.DestinationSceneNotFoundError:
                    raise errors.scenario_machine.NextTransitionNotFoundError(
                        "failed to execute next transition because destination scene not found!"
                        "(chat_id={chat_id!r}, user_id={user_id!r}, source_scene={source_scene!r}, "
                        "handler={handler!r}, direction={direction!r})!",
                        chat_id=chat_id, user_id=user_id, source_scene=source_scene,
                        handler=handler, direction=direction,
                    ) from None

                await self._process_transition(magazine, chat_id=chat_id, user_id=user_id, scene_args=scene_args,
                                               source_scene=source_scene, destination_scene=destination_scene)
        except errors.lock_storage.TransitionLockExistsError:
            if not self._suppress_lock_error:
                raise errors.scenario_machine.TransitionLockedError(
                    "failed to execute next transition because there is an active lock "
                    "(chat_id={chat_id!r}, user_id={user_id!r})!'", chat_id=chat_id, user_id=user_id
                ) from None

    async def execute_back_transition(self, *, chat_id: int, user_id: int, scene_args: Tuple[Any, Any]) -> None:

        try:
            async with self._lock_storage.acquire(chat_id=chat_id, user_id=user_id):
                magazine = await self._state_machine.load_magazine(chat_id=chat_id, user_id=user_id)
                source_scene = self._scene_mapping.get(magazine.current)
                if magazine.previous is None:
                    raise errors.scenario_machine.BackTransitionNotFoundError(
                        "failed to execute back transition because magazine doesn't have a previous scene"
                        "(chat_id={chat_id!r}, user_id={user_id!r}, source_scene={source_scene!r})!",
                        chat_id=chat_id, user_id=user_id, source_scene=source_scene
                    )
                destination_scene = self._scene_mapping.get(magazine.previous)

                await self._process_transition(magazine, chat_id=chat_id, user_id=user_id, scene_args=scene_args,
                                               source_scene=source_scene, destination_scene=destination_scene)
        except errors.lock_storage.TransitionLockExistsError:
            if not self._suppress_lock_error:
                raise errors.scenario_machine.TransitionLockedError(
                    "failed to execute back transition because there is an active lock "
                    "(chat_id={chat_id!r}, user_id={user_id!r})!'", chat_id=chat_id, user_id=user_id
                ) from None

    async def _process_transition(self, magazine: StateMagazine, *,
                                  chat_id: int, user_id: int, scene_args: Tuple[Any, Any],
                                  source_scene: BaseScene, destination_scene: BaseScene) -> None:

        await source_scene.process_exit(*scene_args)
        await destination_scene.process_enter(*scene_args)
        await self._save_state_with_magazine(destination_scene.name, magazine, chat_id=chat_id, user_id=user_id)

    async def _save_state_with_magazine(self, state: str, magazine: StateMagazine, *,
                                        chat_id: int, user_id: int) -> None:

        magazine.set(state)
        await self._state_machine.save_magazine(magazine, chat_id=chat_id, user_id=user_id)
