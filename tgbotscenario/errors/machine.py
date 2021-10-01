from dataclasses import dataclass
from typing import Optional, Callable

from tgbotscenario.errors.base import BaseError
from tgbotscenario.common.scene import BaseScene


@dataclass
class MachineError(BaseError):

    pass


@dataclass
class TransitionNotFoundError(MachineError):

    pass


@dataclass
class NextTransitionNotFoundError(TransitionNotFoundError):

    chat_id: int
    user_id: int
    source_scene: BaseScene
    handler: Callable
    direction: Optional[str]


@dataclass
class BackTransitionNotFoundError(TransitionNotFoundError):

    chat_id: int
    user_id: int
    source_scene: BaseScene


@dataclass
class DoubleTransitionError(MachineError):

    chat_id: int
    user_id: int


@dataclass
class DuplicateSceneNameError(MachineError):

    name: str
