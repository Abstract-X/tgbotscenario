from typing import Dict

from tgbotscenario.common.scenes.scene import BaseScene
from tgbotscenario import errors
import tgbotscenario.errors.scene_mapping


class SceneMapping:

    def __init__(self):

        self._mapping: Dict[str, BaseScene] = {}

    def __getitem__(self, item):

        return self.get(item)

    def add(self, scene: BaseScene) -> None:

        if scene.name in self._mapping:
            existing_scene = self.get(scene.name)
            if existing_scene is not scene:
                raise errors.scene_mapping.SceneNameBusyError(
                    "name {name!r} has already been used to add {existing_scene!r} scene!",
                    name=scene.name, existing_scene=existing_scene
                )

        self._mapping[scene.name] = scene

    def get(self, name: str) -> BaseScene:

        try:
            return self._mapping[name]
        except KeyError:
            raise errors.scene_mapping.SceneNameNotFoundError("scene name {name!r} not found!",
                                                              name=name) from None
