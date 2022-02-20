from dataclasses import dataclass
from typing import Set, TypeVar

from tgbotscenario.common.scene import BaseScene


Scene = TypeVar("Scene")


@dataclass
class BaseScenario:

    def __post_init__(self):
        self._scenes = {i for i in vars(self).values() if isinstance(i, BaseScene)}

    def __len__(self):
        return len(self._scenes)

    def __iter__(self):
        return iter(self._scenes)

    def __repr__(self):
        return f"{type(self).__name__}({self._scenes!r})"

    def __contains__(self, item):
        return item in self._scenes

    def exclude(self, *scenes: Scene) -> Set[Scene]:
        return {i for i in self._scenes if i not in scenes}
