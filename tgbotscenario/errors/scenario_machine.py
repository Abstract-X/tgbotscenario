from dataclasses import dataclass
from typing import Optional, Callable

from tgbotscenario.errors.base import BaseError
from tgbotscenario.types import AbstractSceneUnion


@dataclass
class ScenarioMachineError(BaseError):

    pass


@dataclass
class MigrationToSceneError(ScenarioMachineError):

    chat_id: int
    user_id: int
    scene: AbstractSceneUnion


@dataclass
class TransitionNotFoundError(ScenarioMachineError):

    pass


@dataclass
class NextTransitionNotFoundError(TransitionNotFoundError):

    chat_id: int
    user_id: int
    source_scene: AbstractSceneUnion
    handler: Callable
    direction: Optional[str]


@dataclass
class BackTransitionNotFoundError(TransitionNotFoundError):

    chat_id: int
    user_id: int
    source_scene: AbstractSceneUnion


@dataclass
class TransitionLockedError(ScenarioMachineError):

    chat_id: int
    user_id: int
