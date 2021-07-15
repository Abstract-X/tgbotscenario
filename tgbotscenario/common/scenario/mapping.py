from typing import Dict, Set, Iterable

from tgbotscenario.types import BaseSceneUnion
from tgbotscenario import errors
import tgbotscenario.errors.scene_mapping


class SceneMapping:

    def __init__(self, scenes: Iterable[BaseSceneUnion] = ()):

        self._mapping: Dict[str, BaseSceneUnion] = {}
        for scene in scenes:
            self.add(scene)

    @property
    def scenes(self) -> Set[BaseSceneUnion]:

        return set(self._mapping.values())

    def add(self, scene: BaseSceneUnion) -> None:

        if scene.name in self._mapping:
            existing_scene = self.get(scene.name)
            if existing_scene is not scene:
                raise errors.scene_mapping.SceneNameBusyError(
                    "name {name!r} has already been used to add {existing_scene!r} scene!",
                    name=scene.name, existing_scene=existing_scene
                )
        else:
            self._mapping[scene.name] = scene

    def remove(self, name: str):

        try:
            del self._mapping[name]
        except KeyError:
            raise errors.scene_mapping.SceneNameNotFound("name {name!r} not found!", name=name) from None

    def get(self, name: str) -> BaseSceneUnion:

        try:
            return self._mapping[name]
        except KeyError:
            raise errors.scene_mapping.SceneNameNotFound("name {name!r} not found!", name=name) from None
