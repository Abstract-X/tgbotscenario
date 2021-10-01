from typing import Optional, Tuple

from tgbotscenario.asynchronous.machine import Machine
from tgbotscenario.common.context_data import ContextData
from tgbotscenario.types import TelegramEvent


class ContextMachine:

    def __init__(self, machine: Machine, data: ContextData):

        self._machine = machine
        self._data = data

    async def move_to_next_scene(self, direction: Optional[str] = None, data=None) -> None:

        event, chat_id, user_id = self._get_required_data()
        handler = self._data.handler.get()
        await self._machine.execute_next_transition(event, handler, direction, data,
                                                    chat_id=chat_id, user_id=user_id)

    async def move_to_previous_scene(self, data=None) -> None:

        event, chat_id, user_id = self._get_required_data()
        await self._machine.execute_back_transition(event, data, chat_id=chat_id, user_id=user_id)

    async def refresh_scene(self, data=None) -> None:

        event, chat_id, user_id = self._get_required_data()
        await self._machine.refresh_current_scene(event, data, chat_id=chat_id, user_id=user_id)

    def _get_required_data(self) -> Tuple[TelegramEvent, int, int]:

        event = self._data.event.get()
        chat_id = self._data.chat_id.get()
        user_id = self._data.user_id.get()

        return event, chat_id, user_id
