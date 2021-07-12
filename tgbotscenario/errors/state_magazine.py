from dataclasses import dataclass

from tgbotscenario.errors.base import BaseError


@dataclass
class StateMagazineError(BaseError):

    pass


@dataclass
class StateMagazineInitializationError(BaseError):

    pass
