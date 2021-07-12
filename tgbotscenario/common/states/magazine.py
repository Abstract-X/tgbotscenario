from typing import List, Optional, Iterator

from tgbotscenario import errors
import tgbotscenario.errors.state_magazine


class StateMagazine:

    def __init__(self, states: List[str]):

        if not states:
            raise errors.state_magazine.StateMagazineInitializationError("state magazine can't be empty!")

        self._states = states[:]

    def __eq__(self, other):

        return self._states == other

    def __iter__(self) -> Iterator[str]:

        return iter(self._states)

    def __repr__(self):

        class_name = type(self).__name__
        return f"<{class_name} {self._states}>"

    @property
    def current(self) -> str:

        return self._states[-1]

    @property
    def previous(self) -> Optional[str]:

        try:
            return self._states[-2]
        except IndexError:
            return None

    def set(self, state: str) -> None:

        try:
            index = self._states.index(state)
        except ValueError:  # state not in magazine
            self._states.append(state)
        else:  # state in magazine
            del self._states[index+1:]
