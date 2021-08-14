from dataclasses import dataclass

from tgbotscenario.errors.base import BaseError


@dataclass
class SceneManagerError(BaseError):

    pass


@dataclass
class MagazineLoadingError(SceneManagerError):

    chat_id: int
    user_id: int


@dataclass
class UnknownSceneError(MagazineLoadingError):

    name: str
