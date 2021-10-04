from typing import Set

from tgbotscenario.asynchronous.scenes.storages.base import AbstractSceneStorage
from tgbotscenario.asynchronous.scenes.scene import BaseScene
from tgbotscenario.common.mapping import Mapping
from tgbotscenario.common.magazine import Magazine
from tgbotscenario import errors


class SceneManager:

    def __init__(self, initial_scene: BaseScene, storage: AbstractSceneStorage):

        self._mapping = Mapping()
        self._storage = storage
        self._scenes: Set[BaseScene] = set()
        self._initial_scene = initial_scene
        self.add_scene(initial_scene)

    @property
    def initial_scene(self) -> BaseScene:

        return self._initial_scene

    @property
    def scenes(self) -> Set[BaseScene]:

        return self._scenes.copy()

    def add_scene(self, scene: BaseScene) -> None:

        try:
            self._mapping.add(key=scene.name, value=scene)
        except errors.MappingKeyBusyError as error:
            raise errors.DuplicateSceneNameError(
                "scene name {name!r} is not unique!",
                name=error.key
            )

        self._scenes.add(scene)

    async def load_magazine(self, *, chat_id: int, user_id: int) -> Magazine:

        raw_scenes = await self._storage.load_scenes(chat_id=chat_id, user_id=user_id)
        if raw_scenes:
            try:
                scenes = [self._mapping.get(i) for i in raw_scenes]
            except errors.MappingKeyNotFoundError as error:
                raise errors.UnknownSceneError(
                    "failed to load magazine (chat_id={chat_id!r}, user_id={user_id!r}) because "
                    "the storage contains an unknown scene {scene!r}!",
                    chat_id=chat_id, user_id=user_id, scene=error.key
                ) from None
        else:
            scenes = [self._initial_scene]

        magazine = Magazine(scenes)

        return magazine

    async def save_magazine(self, magazine: Magazine, *, chat_id: int, user_id: int) -> None:

        raw_scenes = [scene.name for scene in magazine]
        await self._storage.save_scenes(raw_scenes, chat_id=chat_id, user_id=user_id)
