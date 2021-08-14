from typing import Optional, Callable, FrozenSet

from tgbotscenario.asynchronous.scenes.base import BaseScene
from tgbotscenario.asynchronous.scenes.storages.base import AbstractSceneStorage
from tgbotscenario.asynchronous.scenes.manager import SceneManager
from tgbotscenario.common.scenes.magazine import SceneMagazine
from tgbotscenario.common.locks.keeper import LockKeeper
from tgbotscenario.common.transition_scheme import TransitionScheme
from tgbotscenario.types import TelegramEvent
from tgbotscenario import errors
import tgbotscenario.errors.scenario_machine
import tgbotscenario.errors.transition_scheme
import tgbotscenario.errors.lock_keeper


class ScenarioMachine:

    def __init__(self, initial_scene: BaseScene, scene_storage: AbstractSceneStorage):

        self._scene_manager = SceneManager(initial_scene, scene_storage)
        self._transition_scheme = TransitionScheme()
        self._lock_keeper = LockKeeper()

    @property
    def initial_scene(self) -> Optional[BaseScene]:

        return self._scene_manager.initial_scene

    @property
    def scenes(self) -> FrozenSet[BaseScene]:

        return self._scene_manager.scenes

    async def get_current_scene(self, *, chat_id: int, user_id: int) -> BaseScene:

        magazine = await self._scene_manager.load_magazine(chat_id=chat_id, user_id=user_id)

        return magazine.current

    def add_transition(self, source_scene: BaseScene, destination_scene: BaseScene,
                       handler: Callable, direction: Optional[str] = None) -> None:

        self._transition_scheme.add_transition(source_scene, destination_scene, handler, direction)
        for scene in (source_scene, destination_scene):
            self._scene_manager.add_scene(scene)

    def check_transition(self, source_scene: BaseScene, destination_scene: BaseScene,
                         handler: Callable, direction: Optional[str] = None) -> bool:

        return self._transition_scheme.check_transition(source_scene, destination_scene, handler, direction)

    async def migrate_to_scene(self, scene: BaseScene, event: TelegramEvent, *, chat_id: int, user_id: int) -> None:

        magazine = await self._scene_manager.load_magazine(chat_id=chat_id, user_id=user_id)

        await scene.process_enter(event)
        magazine.set(scene)

        await self._scene_manager.save_magazine(magazine, chat_id=chat_id, user_id=user_id)
        self._scene_manager.add_scene(scene)

    async def refresh_current_scene(self, event: TelegramEvent, *, chat_id: int, user_id: int) -> None:

        scene = await self.get_current_scene(chat_id=chat_id, user_id=user_id)
        await scene.process_enter(event)

    async def execute_next_transition(self, event: TelegramEvent, handler: Callable,
                                      direction: Optional[str] = None, *, chat_id: int, user_id: int) -> None:

        try:
            with self._lock_keeper.acquire(chat_id=chat_id, user_id=user_id):
                magazine = await self._scene_manager.load_magazine(chat_id=chat_id, user_id=user_id)
                source_scene = magazine.current
                try:
                    destination_scene = self._transition_scheme.get_destination_scene(source_scene, handler, direction)
                except errors.transition_scheme.DestinationSceneNotFoundError:
                    raise errors.scenario_machine.NextTransitionNotFoundError(
                        "failed to execute next transition because destination scene not found! "
                        "(chat_id={chat_id!r}, user_id={user_id!r}, source_scene={source_scene!r}, "
                        "handler={handler!r}, direction={direction!r})!",
                        chat_id=chat_id, user_id=user_id, source_scene=source_scene,
                        handler=handler, direction=direction,
                    ) from None

                await self._process_transition(event, magazine, source_scene, destination_scene,
                                               chat_id=chat_id, user_id=user_id)
        except errors.lock_keeper.TransitionLockExistsError:
            raise errors.scenario_machine.TransitionLockedError(
                "failed to execute next transition because there is an active lock "
                "(chat_id={chat_id!r}, user_id={user_id!r})!",
                chat_id=chat_id, user_id=user_id
            ) from None

    async def execute_back_transition(self, event: TelegramEvent, *, chat_id: int, user_id: int) -> None:

        try:
            with self._lock_keeper.acquire(chat_id=chat_id, user_id=user_id):
                magazine = await self._scene_manager.load_magazine(chat_id=chat_id, user_id=user_id)
                source_scene = magazine.current
                destination_scene = magazine.previous

                if destination_scene is None:
                    raise errors.scenario_machine.BackTransitionNotFoundError(
                        "failed to execute back transition because magazine doesn't have a previous scene "
                        "(chat_id={chat_id!r}, user_id={user_id!r}, source_scene={source_scene!r})!",
                        chat_id=chat_id, user_id=user_id, source_scene=source_scene
                    )

                await self._process_transition(event, magazine, source_scene, destination_scene,
                                               chat_id=chat_id, user_id=user_id)
        except errors.lock_keeper.TransitionLockExistsError:
            raise errors.scenario_machine.TransitionLockedError(
                "failed to execute back transition because there is an active lock "
                "(chat_id={chat_id!r}, user_id={user_id!r})!",
                chat_id=chat_id, user_id=user_id
            ) from None

    async def _process_transition(self, event: TelegramEvent, magazine: SceneMagazine, source_scene: BaseScene,
                                  destination_scene: BaseScene, *, chat_id: int, user_id: int) -> None:

        await source_scene.process_exit(event)
        await destination_scene.process_enter(event)

        if destination_scene is not source_scene:
            magazine.set(destination_scene)
            await self._scene_manager.save_magazine(magazine, chat_id=chat_id, user_id=user_id)
