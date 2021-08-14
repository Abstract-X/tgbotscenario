from typing import Callable
from dataclasses import dataclass
from contextvars import ContextVar

from tgbotscenario.types import TelegramEvent


@dataclass
class ContextData:

    chat_id: ContextVar[int]
    user_id: ContextVar[int]
    handler: ContextVar[Callable]
    event: ContextVar[TelegramEvent]
