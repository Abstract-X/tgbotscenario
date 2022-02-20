from typing import Optional, Tuple, Any

from tgbotscenario.asynchronous.machine import Machine
from tgbotscenario.common.context import Context


class ContextMachine:

    def __init__(self, machine: Machine, context: Context):
        self._machine = machine
        self._context = context

    async def move_to_next_scene(self, direction: Optional[str] = None, data: Any = None) -> None:
        event, chat_id, user_id = self._get_required_data()
        trigger = self._context.trigger.get()
        await self._machine.move_to_next_scene(event, trigger, direction, data,
                                               chat_id=chat_id, user_id=user_id)

    async def move_to_previous_scene(self, data: Any = None) -> None:
        event, chat_id, user_id = self._get_required_data()
        await self._machine.move_to_previous_scene(event, data, chat_id=chat_id, user_id=user_id)

    async def reset_current_scene(self, data: Any = None) -> None:
        event, chat_id, user_id = self._get_required_data()
        await self._machine.reset_current_scene(event, data, chat_id=chat_id, user_id=user_id)

    def _get_required_data(self) -> Tuple[Any, int, int]:
        event = self._context.event.get()
        chat_id = self._context.chat_id.get()
        user_id = self._context.user_id.get()

        return event, chat_id, user_id
