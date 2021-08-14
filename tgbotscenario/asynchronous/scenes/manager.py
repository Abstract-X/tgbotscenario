from typing import Set, FrozenSet

from tgbotscenario.asynchronous.scenes.storages.base import AbstractSceneStorage
from tgbotscenario.asynchronous.scenes.scene import BaseScene
from tgbotscenario.common.scenes.magazine import SceneMagazine
from tgbotscenario.common.scenes.mapping import SceneMapping
from tgbotscenario import errors
import tgbotscenario.errors.scene_mapping
import tgbotscenario.errors.scene_manager


class SceneManager:

    def __init__(self, initial_scene: BaseScene, storage: AbstractSceneStorage):

        self._mapping = SceneMapping()
        self._scenes: Set[BaseScene] = set()
        self._storage = storage
        self._initial_scene = initial_scene
        self.add_scene(initial_scene)

    @property
    def initial_scene(self) -> BaseScene:

        return self._initial_scene

    @property
    def scenes(self) -> FrozenSet[BaseScene]:

        return frozenset(self._scenes)

    def add_scene(self, scene: BaseScene) -> None:

        self._mapping.add(scene)
        self._scenes.add(scene)

    async def load_magazine(self, *, chat_id: int, user_id: int) -> SceneMagazine:

        raw_scenes = await self._storage.load(chat_id=chat_id, user_id=user_id)
        try:
            scenes = [self._mapping[name] for name in raw_scenes]
        except errors.scene_mapping.SceneNameNotFoundError as error:
            raise errors.scene_manager.UnknownSceneError(
                "failed to load magazine (chat_id={chat_id!r}, user_id={user_id!r}) because "
                "the storage contains an unknown scene name {name!r}!",
                chat_id=chat_id, user_id=user_id, name=error.name
            ) from None

        if not scenes:
            scenes = [self._initial_scene]

        return SceneMagazine(scenes)

    async def save_magazine(self, magazine: SceneMagazine, *, chat_id: int, user_id: int) -> None:

        raw_scenes = [scene.name for scene in magazine]
        await self._storage.save(raw_scenes, chat_id=chat_id, user_id=user_id)
