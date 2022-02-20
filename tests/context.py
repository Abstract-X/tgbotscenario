from typing import Callable, Any
from contextvars import ContextVar


chat_id_context: ContextVar[int] = ContextVar("chat_id_context")
user_id_context: ContextVar[int] = ContextVar("user_id_context")
trigger_context: ContextVar[Callable] = ContextVar("trigger_context")
event_context: ContextVar[Any] = ContextVar("event_context")


class ContextVarsContext:

    def __init__(self, chat_id: int, user_id: int, trigger: Callable, event: Any):
        self._chat_id = chat_id
        self._user_id = user_id
        self._trigger = trigger
        self._event = event
        self._tokens = {}

    def __enter__(self):
        self._tokens["chat_id"] = chat_id_context.set(self._chat_id)
        self._tokens["user_id"] = user_id_context.set(self._user_id)
        self._tokens["trigger"] = trigger_context.set(self._trigger)
        self._tokens["event"] = event_context.set(self._event)

    def __exit__(self, exc_type, exc_val, exc_tb):
        chat_id_context.reset(self._tokens["chat_id"])
        user_id_context.reset(self._tokens["user_id"])
        trigger_context.reset(self._tokens["trigger"])
        event_context.reset(self._tokens["event"])
