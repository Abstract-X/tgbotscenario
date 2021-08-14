from typing import Set

from tgbotscenario.common.scenes.base import BaseScene


class ScenarioMixin:

    def __len__(self):

        return len(self._scenes)

    def __iter__(self):

        return iter(self._scenes)

    def __repr__(self):

        return f"<{type(self).__name__} {self._scenes}>"

    def __contains__(self, item):

        return item in self._scenes

    def exclude(self, *scenes: BaseScene) -> Set[BaseScene]:
        return {i for i in self._scenes if i not in scenes}

    @property
    def _scenes(self) -> Set[BaseScene]:

        return {i for i in vars(self).values() if isinstance(i, BaseScene)}
