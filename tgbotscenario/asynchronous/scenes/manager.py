from typing import Set

from tgbotscenario.asynchronous.scenes.storages.base import AbstractSceneStorage
from tgbotscenario.asynchronous.scenes.scene import Scene
from tgbotscenario.common.mapping import Mapping
from tgbotscenario.common.magazine import Magazine
from tgbotscenario import errors


class SceneManager:

    def __init__(self, initial_scene: Scene, storage: AbstractSceneStorage):
        self._mapping = Mapping()
        self._storage = storage
        self._scenes: Set[Scene] = set()
        self._initial_scene = initial_scene
        self.add_scene(initial_scene)

    @property
    def initial_scene(self) -> Scene:
        return self._initial_scene

    @property
    def scenes(self) -> Set[Scene]:
        return self._scenes.copy()

    def add_scene(self, scene: Scene) -> None:
        try:
            self._mapping.add(key=scene.name, value=scene)
        except errors.MappingKeyBusyError as error:
            raise errors.DuplicateSceneNameError(
                "it is not possible to add the scene named {name!r}, "
                "because a scene with the same name has already been added!",
                name=error.key
            ) from None

        self._scenes.add(scene)

    def remove_scene(self, scene: Scene) -> None:
        try:
            self._mapping.remove(key=scene.name, value=scene)
        except errors.MappingDataNotFoundError:
            raise errors.SceneNotFoundError(
                "it is not possible to remove the {scene!r} scene "
                "because it has not been added!",
                scene=scene
            ) from None

        self._scenes.remove(scene)

    async def load_magazine(self, *, chat_id: int, user_id: int) -> Magazine:
        raw_scenes = await self._storage.load_scenes(chat_id=chat_id, user_id=user_id)
        if raw_scenes:
            try:
                scenes = [self._mapping.get_value(i) for i in raw_scenes]
            except errors.MappingKeyNotFoundError as error:
                raise errors.UnknownSceneError(
                    "it is not possible to load the magazine "
                    "(chat_id={chat_id}, user_id={user_id}) "
                    "because the storage contains an unknown {scene!r} scene!",
                    chat_id=chat_id, user_id=user_id, scene=error.key
                ) from None
        else:
            scenes = [self._initial_scene]

        magazine = Magazine(scenes)

        return magazine

    async def save_magazine(self, magazine: Magazine, *, chat_id: int, user_id: int) -> None:
        raw_scenes = [self._mapping.get_key(i) for i in magazine]
        await self._storage.save_scenes(raw_scenes, chat_id=chat_id, user_id=user_id)
