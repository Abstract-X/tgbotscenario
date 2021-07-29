from typing import Callable, Any
from dataclasses import dataclass
from contextvars import ContextVar


@dataclass
class ContextData:

    chat_id: ContextVar[int]
    user_id: ContextVar[int]
    handler: ContextVar[Callable]
    event: ContextVar[Any]
