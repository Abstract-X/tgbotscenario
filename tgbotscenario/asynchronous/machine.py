from typing import Optional, Callable, Set, Any

from tgbotscenario.asynchronous.scenes.scene import Scene
from tgbotscenario.asynchronous.scenes.storages.base import AbstractSceneStorage
from tgbotscenario.asynchronous.scenes.manager import SceneManager
from tgbotscenario.common.transitions.scheme import TransitionScheme
from tgbotscenario.common.transitions.locks.storage import LockStorage
from tgbotscenario.common.transitions.locks.context import LockContext
from tgbotscenario.common.magazine import Magazine
from tgbotscenario import errors


class Machine:

    def __init__(self, initial_scene: Scene, scene_storage: AbstractSceneStorage):
        self._scene_manager = SceneManager(initial_scene, scene_storage)
        self._transition_scheme = TransitionScheme()
        self._lock_storage = LockStorage()

    @property
    def initial_scene(self) -> Scene:
        return self._scene_manager.initial_scene

    @property
    def scenes(self) -> Set[Scene]:
        return self._scene_manager.scenes

    def add_transition(self, source_scene: Scene, destination_scene: Scene,
                       trigger: Callable, direction: Optional[str] = None) -> None:
        for scene in {source_scene, destination_scene}:
            self._scene_manager.add_scene(scene)

        self._transition_scheme.add_transition(source_scene, destination_scene, trigger, direction)

    def check_transition(self, source_scene: Scene, destination_scene: Scene,
                         trigger: Callable, direction: Optional[str] = None) -> bool:
        return self._transition_scheme.check_transition(source_scene, destination_scene,
                                                        trigger, direction)

    def remove_transition(self, source_scene: Scene, trigger: Callable,
                          direction: Optional[str] = None) -> Scene:
        destination_scene = self._transition_scheme.remove_transition(source_scene,
                                                                      trigger, direction)

        for scene in {source_scene, destination_scene}:
            if not self._transition_scheme.check_scene(scene):
                self._scene_manager.remove_scene(scene)

        return destination_scene

    async def get_current_scene(self, *, chat_id: int, user_id: int) -> Scene:
        magazine = await self._scene_manager.load_magazine(chat_id=chat_id, user_id=user_id)

        return magazine.current

    async def set_current_scene(self, scene: Scene, event: Any, data: Any = None,
                                *, chat_id: int, user_id: int) -> None:
        if scene not in self.scenes:
            raise errors.SceneSettingError(
                "it is not possible to set the {scene!r} scene "
                "(chat_id={chat_id}, user_id={user_id}) "
                "because it doesn't participate in the transitions!",
                scene=scene, chat_id=chat_id, user_id=user_id
            )

        try:
            with LockContext(self._lock_storage, chat_id=chat_id, user_id=user_id):
                magazine = await self._scene_manager.load_magazine(chat_id=chat_id,
                                                                   user_id=user_id)
                await scene.process_enter(event, data)
                await self._apply_scene(scene, magazine, chat_id=chat_id, user_id=user_id)
        except errors.LockExistsError:
            raise errors.SceneSettingError(
                "it is not possible to set the {scene!r} scene "
                "(chat_id={chat_id}, user_id={user_id}) "
                "because a transition in progress!",
                chat_id=chat_id, user_id=user_id, scene=scene
            ) from None

    async def reset_current_scene(self, event: Any, data: Any = None,
                                  *, chat_id: int, user_id: int) -> None:
        scene = await self.get_current_scene(chat_id=chat_id, user_id=user_id)
        await scene.process_enter(event, data)

    async def move_to_next_scene(self, event: Any, trigger: Callable,
                                 direction: Optional[str] = None, data: Any = None,
                                 *, chat_id: int, user_id: int) -> None:
        try:
            with LockContext(self._lock_storage, chat_id=chat_id, user_id=user_id):
                magazine = await self._scene_manager.load_magazine(chat_id=chat_id,
                                                                   user_id=user_id)
                try:
                    next_scene = self._transition_scheme.get_destination_scene(
                        magazine.current, trigger, direction
                    )
                except errors.DestinationSceneNotFoundError:
                    raise errors.TransitionToNextSceneError(
                        "it is not possible to move to the next scene "
                        "(chat_id={chat_id}, user_id={user_id}, current_scene={current_scene!r}, "
                        "trigger={trigger!r}, direction={direction!r}) "
                        "because it has not been set!",
                        chat_id=chat_id, user_id=user_id, current_scene=magazine.current,
                        trigger=trigger, direction=direction
                    ) from None

                await self._process_transition(event, data, magazine, magazine.current,
                                               next_scene, chat_id=chat_id,
                                               user_id=user_id)
        except errors.LockExistsError:
            raise errors.DoubleTransitionError(
                "it is not possible to move to the next scene "
                "(chat_id={chat_id}, user_id={user_id}) "
                "because an another transition in progress!",
                chat_id=chat_id, user_id=user_id
            ) from None

    async def move_to_previous_scene(self, event: Any, data: Any = None,
                                     *, chat_id: int, user_id: int) -> None:
        try:
            with LockContext(self._lock_storage, chat_id=chat_id, user_id=user_id):
                magazine = await self._scene_manager.load_magazine(chat_id=chat_id,
                                                                   user_id=user_id)
                if magazine.previous is None:
                    raise errors.TransitionToPreviousSceneError(
                        "it is not possible to move to the previous scene "
                        "(chat_id={chat_id}, user_id={user_id}, current_scene={current_scene!r}) "
                        "because the current scene is the initial scene!",
                        chat_id=chat_id, user_id=user_id, current_scene=magazine.current
                    )
                await self._process_transition(event, data, magazine, magazine.current,
                                               magazine.previous, chat_id=chat_id,
                                               user_id=user_id)
        except errors.LockExistsError:
            raise errors.DoubleTransitionError(
                "it is not possible to move to the previous scene "
                "(chat_id={chat_id}, user_id={user_id}) "
                "because an another transition in progress!",
                chat_id=chat_id, user_id=user_id
            ) from None

    async def _process_transition(self, event: Any, data: Any, magazine: Magazine,
                                  source_scene: Scene, destination_scene: Scene,
                                  *, chat_id: int, user_id: int) -> None:
        await source_scene.process_exit(event, data)
        await destination_scene.process_enter(event, data)
        await self._apply_scene(destination_scene, magazine, chat_id=chat_id, user_id=user_id)

    async def _apply_scene(self, scene: Scene, magazine: Magazine,
                           *, chat_id: int, user_id: int) -> None:
        magazine.set(scene)
        await self._scene_manager.save_magazine(magazine, chat_id=chat_id, user_id=user_id)
