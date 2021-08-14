from typing import Callable
from contextvars import ContextVar

import pytest

from tgbotscenario.common.context_data import ContextData
from tgbotscenario.types import TelegramEvent


chat_id_context: ContextVar[int] = ContextVar("chat_id_context")
user_id_context: ContextVar[int] = ContextVar("user_id_context")
handler_context: ContextVar[Callable] = ContextVar("handler_context")
event_context: ContextVar[TelegramEvent] = ContextVar("event_context")


@pytest.fixture()
def chat_id():

    return -1001234567890


@pytest.fixture()
def user_id():

    return 1234567890


@pytest.fixture()
def event():

    return object()


@pytest.fixture()
def handler():

    def handler():
        pass

    return handler


@pytest.fixture()
def context_data(chat_id, user_id, handler, event):

    data = ContextData(chat_id=chat_id_context, user_id=user_id_context, handler=handler_context, event=event_context)

    chat_id_token = chat_id_context.set(chat_id)
    user_id_token = user_id_context.set(user_id)
    handler_token = handler_context.set(handler)
    event_token = event_context.set(event)

    yield data

    chat_id_context.reset(chat_id_token)
    user_id_context.reset(user_id_token)
    handler_context.reset(handler_token)
    event_context.reset(event_token)
