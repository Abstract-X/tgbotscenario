from typing import TYPE_CHECKING, List

from tgbotscenario.asynchronous.states.storages.base import AbstractStateStorage

if TYPE_CHECKING:
    try:
        from motor.motor_asyncio import AsyncIOMotorDatabase
    except ModuleNotFoundError as e:
        import warnings

        warnings.warn("Install motor with `pip install motor`")
        raise e


class MongoStateStorage(AbstractStateStorage):
    def __init__(self, db: AsyncIOMotorDatabase, collection: str = "state_storage"):
        self._db = db
        self._collection = db[collection]

    async def apply_index(self):
        self._collection.create_index(
            keys=[("chat", 1), ("user", 1)],
            name="chat_user_idx",
            unique=True,
            background=True,
        )

    async def load(self, *, chat_id: int, user_id: int) -> List[str]:
        result = await self._collection.find_one({"chat": chat_id, "user": user_id})
        if result is None:
            return []
        return result["states"]

    async def save(self, states: List[str], *, chat_id: int, user_id: int) -> None:
        await self._collection.update_one(
            {"chat": chat_id, "user": user_id},
            {"$set": {"states": states}},
            upsert=True,
        )
