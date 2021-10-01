from abc import ABC, abstractmethod
from typing import List


class AbstractSceneStorage(ABC):

    @abstractmethod
    async def load_scenes(self, *, chat_id: int, user_id: int) -> List[str]:

        pass

    @abstractmethod
    async def save_scenes(self, scenes: List[str], *, chat_id: int, user_id: int) -> None:

        pass
