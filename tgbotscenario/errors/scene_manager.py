from dataclasses import dataclass

from tgbotscenario.errors.base import BaseError


@dataclass
class SceneManagerError(BaseError):

    pass


@dataclass
class UnknownSceneError(SceneManagerError):

    chat_id: int
    user_id: int
    scene: str
