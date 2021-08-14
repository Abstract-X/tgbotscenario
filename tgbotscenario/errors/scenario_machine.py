from dataclasses import dataclass
from typing import Optional, Callable

from tgbotscenario.errors.base import BaseError
from tgbotscenario.common.scenes.scene import BaseScene


@dataclass
class ScenarioMachineError(BaseError):

    pass


@dataclass
class TransitionNotFoundError(ScenarioMachineError):

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
class TransitionLockedError(ScenarioMachineError):

    chat_id: int
    user_id: int
