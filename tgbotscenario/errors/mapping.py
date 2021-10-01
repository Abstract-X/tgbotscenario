from dataclasses import dataclass
from typing import Any

from tgbotscenario.errors.base import BaseError


@dataclass
class MappingError(BaseError):

    pass


@dataclass
class KeyBusyError(MappingError):

    key: str
    existing_value: Any


@dataclass
class KeyNotFoundError(MappingError):

    key: str
