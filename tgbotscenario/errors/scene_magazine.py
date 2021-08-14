from dataclasses import dataclass

from tgbotscenario.errors.base import BaseError


@dataclass
class SceneMagazineError(BaseError):

    pass


@dataclass
class SceneMagazineInitializationError(SceneMagazineError):

    pass
