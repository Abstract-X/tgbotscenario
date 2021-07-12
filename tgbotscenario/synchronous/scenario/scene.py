from abc import ABCMeta, abstractmethod

from tgbotscenario.common.scenario.scene import BaseScene


class AbstractScene(BaseScene, metaclass=ABCMeta):

    @abstractmethod
    def process_enter(self, *args) -> None:

        pass

    @abstractmethod
    def process_exit(self, *args) -> None:

        pass
