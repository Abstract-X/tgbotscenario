from typing import Iterator

from tgbotscenario.types import AbstractSceneUnion


class SceneSet:

    def __init__(self, *scenes: AbstractSceneUnion):

        self._set = frozenset(scenes)

    def __iter__(self) -> Iterator[AbstractSceneUnion]:

        return iter(self._set)

    def __eq__(self, other):

        return self._set == other

    def __hash__(self):

        return hash(self._set)
