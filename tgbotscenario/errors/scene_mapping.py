from dataclasses import dataclass

from tgbotscenario.errors.base import BaseError
from tgbotscenario.common.scenes.scene import BaseScene


@dataclass
class SceneMappingError(BaseError):

    pass


@dataclass
class SceneNameBusyError(SceneMappingError):

    name: str
    existing_scene: BaseScene


@dataclass
class SceneNameNotFoundError(SceneMappingError):

    name: str
