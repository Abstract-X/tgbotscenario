from dataclasses import dataclass
from typing import Optional, Callable

from tgbotscenario.errors.base import BaseError
from tgbotscenario.types import BaseSceneUnion


@dataclass
class ScenarioMachineError(BaseError):

    pass


@dataclass
class MigrationToSceneError(ScenarioMachineError):

    chat_id: int
    user_id: int
    scene: BaseSceneUnion


@dataclass
class TransitionNotFoundError(ScenarioMachineError):

    pass


@dataclass
class NextTransitionNotFoundError(TransitionNotFoundError):

    chat_id: int
    user_id: int
    source_scene: BaseSceneUnion
    handler: Callable
    direction: Optional[str]


@dataclass
class BackTransitionNotFoundError(TransitionNotFoundError):

    chat_id: int
    user_id: int
    source_scene: BaseSceneUnion


@dataclass
class TransitionLockedError(ScenarioMachineError):

    chat_id: int
    user_id: int
