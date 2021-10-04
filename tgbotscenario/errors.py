from dataclasses import dataclass
from typing import Dict, Any, Optional, Callable

from tgbotscenario.common.scene import BaseScene


@dataclass
class BaseError(Exception):

    raw_message: str

    def __post_init__(self):

        self._format_kwargs = self._get_format_kwargs()

    def __str__(self):

        return self.raw_message.format(**self._format_kwargs)

    def _get_format_kwargs(self) -> Dict[str, Any]:

        kwargs = vars(self).copy()
        del kwargs["raw_message"]

        return kwargs


@dataclass
class TransitionNotFoundError(BaseError):

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
class DoubleTransitionError(BaseError):

    chat_id: int
    user_id: int


@dataclass
class DuplicateSceneNameError(BaseError):

    name: str


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
    existing_value: Any


@dataclass
class MappingKeyNotFoundError(BaseError):

    key: str


@dataclass
class DestinationSceneNotFoundError(BaseError):

    source_scene: BaseScene
    handler: Callable
    direction: Optional[str]


@dataclass
class TransitionExistsError(BaseError):

    source_scene: BaseScene
    destination_scene: BaseScene
    handler: Callable
    direction: Optional[str]


@dataclass
class TransitionBusyError(BaseError):

    source_scene: BaseScene
    destination_scene: BaseScene
    handler: Callable
    direction: Optional[str]
    existing_destination_scene: BaseScene


@dataclass
class SceneSetError(BaseError):

    chat_id: int
    user_id: int
    scene: BaseScene


@dataclass
class SceneNotFoundError(BaseError):

    name: str
