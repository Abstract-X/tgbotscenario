from __future__ import annotations
from typing import Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from tgbotscenario.types import BaseSceneUnion


class SceneSet:

    def __init__(self, *scenes: BaseSceneUnion):

        self._set = frozenset(scenes)

    def __iter__(self) -> Iterator[BaseSceneUnion]:

        return iter(self._set)

    def __eq__(self, other):

        return self._set == other

    def __hash__(self):

        return hash(self._set)
