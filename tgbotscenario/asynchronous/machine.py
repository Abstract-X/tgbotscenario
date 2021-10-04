from typing import Optional, Callable, Set

from tgbotscenario.asynchronous.scenes.scene import BaseScene
from tgbotscenario.asynchronous.scenes.storages.base import AbstractSceneStorage
from tgbotscenario.asynchronous.scenes.manager import SceneManager
from tgbotscenario.common.transitions.scheme import TransitionScheme
from tgbotscenario.common.transitions.locks.storage import LockStorage
from tgbotscenario.common.transitions.locks.context import LockContext
from tgbotscenario.common.magazine import Magazine
from tgbotscenario.types import TelegramEvent
from tgbotscenario import errors


class Machine:

    def __init__(self, initial_scene: BaseScene, scene_storage: AbstractSceneStorage):

        self._scene_manager = SceneManager(initial_scene, scene_storage)
        self._transition_scheme = TransitionScheme()
        self._lock_storage = LockStorage()

    @property
    def initial_scene(self) -> BaseScene:

        return self._scene_manager.initial_scene

    @property
    def scenes(self) -> Set[BaseScene]:

        return self._scene_manager.scenes

    def add_transition(self, source_scene: BaseScene, destination_scene: BaseScene,
                       handler: Callable, direction: Optional[str] = None) -> None:

        self._transition_scheme.add_transition(source_scene, destination_scene, handler, direction)
        for scene in (source_scene, destination_scene):
            self._add_scene(scene)

    def check_transition(self, source_scene: BaseScene, destination_scene: BaseScene,
                         handler: Callable, direction: Optional[str] = None) -> bool:

        return self._transition_scheme.check_transition(source_scene, destination_scene, handler, direction)

    async def get_current_scene(self, *, chat_id: int, user_id: int) -> BaseScene:

        magazine = await self._scene_manager.load_magazine(chat_id=chat_id, user_id=user_id)

        return magazine.current

    async def refresh_current_scene(self, event: TelegramEvent, data=None,
                                    *, chat_id: int, user_id: int) -> None:

        scene = await self.get_current_scene(chat_id=chat_id, user_id=user_id)
        await scene.process_enter(event, data)

    async def set_current_scene(self, scene: BaseScene, event: TelegramEvent, data=None,
                                *, chat_id: int, user_id: int) -> None:

        if scene not in self.scenes:
            raise errors.SceneSetError(
                "scene {scene!r} (chat_id={chat_id!r}, user_id={user_id!r}) cannot be set "
                "because it does not participate in transitions!",
                chat_id=chat_id, user_id=user_id, scene=scene
            )

        try:
            with LockContext(self._lock_storage, chat_id=chat_id, user_id=user_id):
                magazine = await self._scene_manager.load_magazine(chat_id=chat_id, user_id=user_id)
                await scene.process_enter(event, data)
                magazine.set(scene)
                await self._scene_manager.save_magazine(magazine, chat_id=chat_id, user_id=user_id)
        except errors.LockExistsError:
            raise errors.SceneSetError(
                "scene {scene!r} (chat_id={chat_id!r}, user_id={user_id!r}) cannot be set "
                "because transition in progress!",
                chat_id=chat_id, user_id=user_id, scene=scene
            ) from None

    async def execute_next_transition(self, event: TelegramEvent, handler: Callable,
                                      direction: Optional[str] = None, data=None,
                                      *, chat_id: int, user_id: int) -> None:

        try:
            with LockContext(self._lock_storage, chat_id=chat_id, user_id=user_id):
                magazine = await self._scene_manager.load_magazine(chat_id=chat_id, user_id=user_id)
                source_scene = magazine.current
                try:
                    destination_scene = self._transition_scheme.get_destination_scene(source_scene, handler, direction)
                except errors.DestinationSceneNotFoundError:
                    raise errors.NextTransitionNotFoundError(
                        "failed to execute next transition because destination scene not found! "
                        "(chat_id={chat_id!r}, user_id={user_id!r}, source_scene={source_scene!r}, "
                        "handler={handler!r}, direction={direction!r})!",
                        chat_id=chat_id, user_id=user_id, source_scene=source_scene,
                        handler=handler, direction=direction,
                    ) from None

                await self._process_transition(event, data, magazine, source_scene, destination_scene,
                                               chat_id=chat_id, user_id=user_id)
        except errors.LockExistsError:
            raise errors.DoubleTransitionError(
                "unable to execute next transition while another transition is in progress "
                "(chat_id={chat_id!r}, user_id={user_id!r})!",
                chat_id=chat_id, user_id=user_id
            ) from None

    async def execute_back_transition(self, event: TelegramEvent, data=None,
                                      *, chat_id: int, user_id: int) -> None:

        try:
            with LockContext(self._lock_storage, chat_id=chat_id, user_id=user_id):
                magazine = await self._scene_manager.load_magazine(chat_id=chat_id, user_id=user_id)
                source_scene = magazine.current
                destination_scene = magazine.previous

                if destination_scene is None:
                    raise errors.BackTransitionNotFoundError(
                        "failed to execute back transition because magazine doesn't have a previous scene "
                        "(chat_id={chat_id!r}, user_id={user_id!r}, source_scene={source_scene!r})!",
                        chat_id=chat_id, user_id=user_id, source_scene=source_scene
                    )

                await self._process_transition(event, data, magazine, source_scene, destination_scene,
                                               chat_id=chat_id, user_id=user_id)
        except errors.LockExistsError:
            raise errors.DoubleTransitionError(
                "unable to execute back transition while another transition is in progress "
                "(chat_id={chat_id!r}, user_id={user_id!r})!",
                chat_id=chat_id, user_id=user_id
            ) from None

    async def _process_transition(self, event: TelegramEvent, data, magazine: Magazine, source_scene: BaseScene,
                                  destination_scene: BaseScene, *, chat_id: int, user_id: int) -> None:

        await source_scene.process_exit(event, data)
        await destination_scene.process_enter(event, data)

        magazine.set(destination_scene)
        await self._scene_manager.save_magazine(magazine, chat_id=chat_id, user_id=user_id)

    def _add_scene(self, scene: BaseScene) -> None:

        try:
            self._scene_manager.add_scene(scene)
        except errors.MappingKeyBusyError as error:
            raise errors.DuplicateSceneNameError(
                "transition with another scene named {name!r} has already been added earlier!",
                name=error.key
            )
