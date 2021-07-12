from abc import ABC, abstractmethod
from typing import List


class AbstractStateStorage(ABC):

    @abstractmethod
    async def load(self, *, chat_id: int, user_id: int) -> List[str]:

        pass

    @abstractmethod
    async def save(self, states: List[str], *, chat_id: int, user_id: int) -> None:

        pass
