from typing import Callable
from contextvars import ContextVar

from tgbotscenario.types import TelegramEvent


chat_id_context: ContextVar[int] = ContextVar("chat_id_context")
user_id_context: ContextVar[int] = ContextVar("user_id_context")
handler_context: ContextVar[Callable] = ContextVar("handler_context")
event_context: ContextVar[TelegramEvent] = ContextVar("event_context")


class Context:

    def __init__(self, chat_id: int, user_id: int, handler: Callable, event: TelegramEvent):

        self._chat_id = chat_id
        self._user_id = user_id
        self._handler = handler
        self._event = event
        self._tokens = {}

    def __enter__(self):

        chat_id_token = chat_id_context.set(self._chat_id)
        user_id_token = user_id_context.set(self._user_id)
        handler_token = handler_context.set(self._handler)
        event_token = event_context.set(self._event)

        self._tokens["chat_id"] = chat_id_token
        self._tokens["user_id"] = user_id_token
        self._tokens["handler"] = handler_token
        self._tokens["event_token"] = event_token

    def __exit__(self, exc_type, exc_val, exc_tb):

        chat_id_context.reset(self._tokens["chat_id"])
        user_id_context.reset(self._tokens["user_id"])
        handler_context.reset(self._tokens["handler"])
        event_context.reset(self._tokens["event_token"])
