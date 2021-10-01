from dataclasses import dataclass

from tgbotscenario.errors.base import BaseError


@dataclass
class LockStorageError(BaseError):

    pass


@dataclass
class LockExistsError(LockStorageError):

    chat_id: int
    user_id: int
