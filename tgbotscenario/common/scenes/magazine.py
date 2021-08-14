from typing import List, Optional, Iterator

from tgbotscenario.common.scenes.scene import BaseScene
from tgbotscenario import errors
import tgbotscenario.errors.scene_magazine


class SceneMagazine:

    def __init__(self, scenes: List[BaseScene]):

        if not scenes:
            raise errors.scene_magazine.SceneMagazineInitializationError("scene magazine can't be empty!")

        self._scenes = scenes[:]

    def __eq__(self, other):

        return self._scenes == other

    def __iter__(self) -> Iterator[BaseScene]:

        return iter(self._scenes)

    def __repr__(self):

        class_name = type(self).__name__
        return f"<{class_name} {self._scenes}>"

    @property
    def current(self) -> BaseScene:

        return self._scenes[-1]

    @property
    def previous(self) -> Optional[BaseScene]:

        try:
            return self._scenes[-2]
        except IndexError:
            return None

    def set(self, scene: BaseScene) -> None:

        try:
            index = self._scenes.index(scene)
        except ValueError:  # scene not in magazine
            self._scenes.append(scene)
        else:  # scene in magazine
            del self._scenes[index+1:]
