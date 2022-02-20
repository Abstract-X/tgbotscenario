from typing import Callable, Any
from dataclasses import dataclass
from contextvars import ContextVar


@dataclass
class Context:
    chat_id: ContextVar[int]
    user_id: ContextVar[int]
    trigger: ContextVar[Callable]
    event: ContextVar[Any]
