from dataclasses import dataclass
from typing import Optional, Callable

from tgbotscenario.errors.base import BaseError
from tgbotscenario.types import AbstractSceneUnion


@dataclass
class TransitionStorageError(BaseError):

    pass


@dataclass
class DestinationSceneNotFoundError(TransitionStorageError):

    source_scene: AbstractSceneUnion
    handler: Callable
    direction: Optional[str]


@dataclass
class TransitionExistsError(TransitionStorageError):

    source_scene: AbstractSceneUnion
    destination_scene: AbstractSceneUnion
    handler: Callable
    direction: Optional[str]


@dataclass
class TransitionBusyError(TransitionStorageError):

    source_scene: AbstractSceneUnion
    destination_scene: AbstractSceneUnion
    handler: Callable
    direction: Optional[str]
    existing_destination_scene: AbstractSceneUnion


@dataclass
class TransitionForRemovingNotFoundError(TransitionStorageError):

    source_scene: AbstractSceneUnion
    handler: Callable
    direction: Optional[str]
