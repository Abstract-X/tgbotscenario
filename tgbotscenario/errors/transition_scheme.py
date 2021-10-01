from dataclasses import dataclass
from typing import Optional, Callable

from tgbotscenario.errors.base import BaseError
from tgbotscenario.common.scene import BaseScene


@dataclass
class TransitionSchemeError(BaseError):

    pass


@dataclass
class DestinationSceneNotFoundError(TransitionSchemeError):

    source_scene: BaseScene
    handler: Callable
    direction: Optional[str]


@dataclass
class TransitionExistsError(TransitionSchemeError):

    source_scene: BaseScene
    destination_scene: BaseScene
    handler: Callable
    direction: Optional[str]


@dataclass
class TransitionBusyError(TransitionSchemeError):

    source_scene: BaseScene
    destination_scene: BaseScene
    handler: Callable
    direction: Optional[str]
    existing_destination_scene: BaseScene
