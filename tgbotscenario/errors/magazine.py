from dataclasses import dataclass

from tgbotscenario.errors.base import BaseError


@dataclass
class MagazineError(BaseError):

    pass


@dataclass
class MagazineInitializationError(MagazineError):

    pass
