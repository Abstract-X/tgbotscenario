from dataclasses import dataclass
from typing import Any, Optional, Callable

from xcept import Exception_

from tgbotscenario.common.scene import BaseScene


@dataclass
class BaseError(Exception_):
    pass


@dataclass
class TransitionError(BaseError):
    pass


@dataclass
class TransitionToNextSceneError(TransitionError):
    chat_id: int
    user_id: int
    current_scene: BaseScene
    trigger: Callable
    direction: Optional[str]


@dataclass
class TransitionToPreviousSceneError(TransitionError):
    chat_id: int
    user_id: int
    current_scene: BaseScene


@dataclass
class DoubleTransitionError(TransitionError):
    chat_id: int
    user_id: int


@dataclass
class DuplicateSceneNameError(BaseError):
    name: str


@dataclass
class TransitionForRemovingNotFoundError(BaseError):
    source_scene: BaseScene
    trigger: Callable
    direction: Optional[str]


@dataclass
class LockExistsError(BaseError):
    chat_id: int
    user_id: int


@dataclass
class MagazineInitializationError(BaseError):
    pass


@dataclass
class UnknownSceneError(BaseError):
    chat_id: int
    user_id: int
    scene: str


@dataclass
class MappingKeyBusyError(BaseError):
    key: str
    value: Any
    existing_value: Any


@dataclass
class MappingValueBusyError(BaseError):
    value: Any
    key: str
    existing_key: str


@dataclass
class MappingDataNotFoundError(BaseError):
    key: str
    value: Any


@dataclass
class MappingKeyNotFoundError(BaseError):
    key: str


@dataclass
class MappingValueNotFoundError(BaseError):
    value: Any


@dataclass
class DestinationSceneNotFoundError(BaseError):
    source_scene: BaseScene
    trigger: Callable
    direction: Optional[str]


@dataclass
class TransitionExistsError(BaseError):
    source_scene: BaseScene
    destination_scene: BaseScene
    trigger: Callable
    direction: Optional[str]


@dataclass
class TransitionBusyError(BaseError):
    source_scene: BaseScene
    destination_scene: BaseScene
    trigger: Callable
    direction: Optional[str]
    existing_destination_scene: BaseScene


@dataclass
class SceneSettingError(BaseError):
    scene: BaseScene
    chat_id: int
    user_id: int


@dataclass
class SceneNotFoundError(BaseError):
    scene: BaseScene
