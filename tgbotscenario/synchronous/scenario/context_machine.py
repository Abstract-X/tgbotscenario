from typing import Optional

from tgbotscenario.synchronous.scenario.machine import ScenarioMachine
from tgbotscenario.common.scenario.context_data import ContextData


class ContextMachine:

    def __init__(self, machine: ScenarioMachine, data: ContextData):

        self._machine = machine
        self._data = data

    def move_to_next_scene(self, direction: Optional[str] = None) -> None:

        chat_id = self._data.chat_id.get()
        user_id = self._data.user_id.get()
        handler = self._data.handler.get()
        event = self._data.event.get()

        self._machine.execute_next_transition(event, chat_id=chat_id, user_id=user_id,
                                              handler=handler, direction=direction)

    def move_to_previous_scene(self) -> None:

        chat_id = self._data.chat_id.get()
        user_id = self._data.user_id.get()
        event = self._data.event.get()

        self._machine.execute_back_transition(event, chat_id=chat_id, user_id=user_id)

    def refresh_scene(self) -> None:

        chat_id = self._data.chat_id.get()
        user_id = self._data.user_id.get()
        event = self._data.event.get()

        self._machine.refresh_current_scene(event, chat_id=chat_id, user_id=user_id)
