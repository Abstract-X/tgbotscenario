from typing import Iterable, Set

from tgbotscenario.types import BaseSceneUnion
from tgbotscenario.common.scenario.scene import BaseScene


class BaseScenario:

    def __init__(self):

        self._scenes = {i for i in vars(type(self)).values() if isinstance(i, BaseScene)}

    def __len__(self):

        return len(self._scenes)

    def __iter__(self):

        return iter(self._scenes)

    def __repr__(self):

        return f"<{type(self).__name__} {self._scenes}>"

    def __contains__(self, item):

        return item in self._scenes

    def select(self, *, exclude: Iterable[BaseSceneUnion] = ()) -> Set[BaseSceneUnion]:

        return {i for i in self._scenes if i not in exclude}
