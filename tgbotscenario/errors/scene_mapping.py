from dataclasses import dataclass

from tgbotscenario.errors.base import BaseError
from tgbotscenario.types import AbstractSceneUnion


@dataclass
class SceneMappingError(BaseError):

    pass


@dataclass
class SceneNameBusyError(SceneMappingError):

    name: str
    existing_scene: AbstractSceneUnion


@dataclass
class SceneNameNotFound(SceneMappingError):

    name: str
