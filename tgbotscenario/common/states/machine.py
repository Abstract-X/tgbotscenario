from typing import Optional


class BaseStateMachine:

    def __init__(self, initial_state: str):

        self._initial_state = initial_state

    @property
    def initial_state(self) -> Optional[str]:

        return self._initial_state
