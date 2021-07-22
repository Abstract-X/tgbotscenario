from typing import Optional

from tgbotscenario.synchronous.states.storages.base import AbstractStateStorage
from tgbotscenario.common.states.magazine import StateMagazine


class StateMachine:

    def __init__(self, initial_state: str, state_storage: AbstractStateStorage):

        self._initial_state = initial_state
        self._state_storage = state_storage

    @property
    def initial_state(self) -> Optional[str]:

        return self._initial_state

    def get_current_state(self, *, chat_id: int, user_id: int) -> str:

        magazine = self.load_magazine(chat_id=chat_id, user_id=user_id)

        return magazine.current

    def set_current_state(self, state: str, *, chat_id: int, user_id: int) -> None:

        magazine = self.load_magazine(chat_id=chat_id, user_id=user_id)
        magazine.set(state)
        self.save_magazine(magazine, chat_id=chat_id, user_id=user_id)

    def load_magazine(self, *, chat_id: int, user_id: int) -> StateMagazine:

        states = self._state_storage.load(chat_id=chat_id, user_id=user_id)
        if not states:
            states = [self.initial_state]

        magazine = StateMagazine(states)

        return magazine

    def save_magazine(self, magazine: StateMagazine, *, chat_id: int, user_id: int) -> None:

        self._state_storage.save(list(magazine), chat_id=chat_id, user_id=user_id)
