from dataclasses import dataclass

from tgbotscenario.common.scene import BaseScene


@dataclass
class BaseScenario:

    def __post_init__(self):

        self._scenes = {i for i in vars(self).values() if isinstance(i, BaseScene)}

    def __len__(self):

        return len(self._scenes)

    def __iter__(self):

        return iter(self._scenes)

    def __repr__(self):

        return f"<{type(self).__name__} {self._scenes}>"

    def __contains__(self, item):

        return item in self._scenes
