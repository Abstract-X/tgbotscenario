from dataclasses import dataclass

from tgbotscenario.errors.base import BaseError
from tgbotscenario.types import BaseSceneUnion


@dataclass
class SceneMappingError(BaseError):

    pass


@dataclass
class SceneNameBusyError(SceneMappingError):

    name: str
    existing_scene: BaseSceneUnion


@dataclass
class SceneNameNotFoundError(SceneMappingError):

    name: str
