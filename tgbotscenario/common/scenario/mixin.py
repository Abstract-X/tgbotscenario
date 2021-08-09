from typing import Set

from tgbotscenario.types import BaseSceneUnion
from tgbotscenario.common.scenario.scene import BaseScene


class ScenarioMixin:

    def __len__(self):

        return len(self._scenes)

    def __iter__(self):

        return iter(self._scenes)

    def __repr__(self):

        return f"<{type(self).__name__} {self._scenes}>"

    def __contains__(self, item):

        return item in self._scenes

    def exclude(self, *scenes: BaseSceneUnion) -> Set[BaseSceneUnion]:
        return {i for i in self._scenes if i not in scenes}

    @property
    def _scenes(self) -> Set[BaseSceneUnion]:

        return {i for i in vars(self).values() if isinstance(i, BaseScene)}
