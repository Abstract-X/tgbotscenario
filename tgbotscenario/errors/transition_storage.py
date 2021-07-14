from dataclasses import dataclass
from typing import Optional, Callable

from tgbotscenario.errors.base import BaseError
from tgbotscenario.types import BaseSceneUnion


@dataclass
class TransitionStorageError(BaseError):

    pass


@dataclass
class DestinationSceneNotFoundError(TransitionStorageError):

    source_scene: BaseSceneUnion
    handler: Callable
    direction: Optional[str]


@dataclass
class TransitionExistsError(TransitionStorageError):

    source_scene: BaseSceneUnion
    destination_scene: BaseSceneUnion
    handler: Callable
    direction: Optional[str]


@dataclass
class TransitionBusyError(TransitionStorageError):

    source_scene: BaseSceneUnion
    destination_scene: BaseSceneUnion
    handler: Callable
    direction: Optional[str]
    existing_destination_scene: BaseSceneUnion


@dataclass
class TransitionForRemovingNotFoundError(TransitionStorageError):

    source_scene: BaseSceneUnion
    handler: Callable
    direction: Optional[str]
