from typing import Optional, Any

from tgbotscenario.asynchronous.scenario.machine import ScenarioMachine
from tgbotscenario.common.scenario.context_data import ContextData


class ContextMachine:

    def __init__(self, machine: ScenarioMachine, context_data: ContextData, scene_data: Any = None):

        self._machine = machine
        self._context_data = context_data
        self._scene_data = scene_data

    async def move_to_next_scene(self, direction: Optional[str] = None) -> None:

        chat_id = self._context_data.chat_id.get()
        user_id = self._context_data.user_id.get()
        handler = self._context_data.handler.get()
        event = self._context_data.event.get()

        await self._machine.execute_next_transition(chat_id=chat_id, user_id=user_id,
                                                    scene_args=(event, self._scene_data), handler=handler,
                                                    direction=direction)

    async def move_to_previous_scene(self) -> None:

        chat_id = self._context_data.chat_id.get()
        user_id = self._context_data.user_id.get()
        event = self._context_data.event.get()

        await self._machine.execute_back_transition(chat_id=chat_id, user_id=user_id,
                                                    scene_args=(event, self._scene_data))

    async def refresh_scene(self) -> None:

        chat_id = self._context_data.chat_id.get()
        user_id = self._context_data.user_id.get()
        event = self._context_data.event.get()
        current_scene = await self._machine.get_current_scene(chat_id=chat_id, user_id=user_id)

        await current_scene.process_enter(event, self._scene_data)
