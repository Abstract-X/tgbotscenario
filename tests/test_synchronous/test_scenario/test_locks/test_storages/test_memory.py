from tgbotscenario.synchronous.scenario.locks.storages.memory import MemoryLockStorage


class TestMemoryLockStorageSet:

    def test(self, chat_id, user_id):

        storage = MemoryLockStorage()
        storage.set(chat_id=chat_id, user_id=user_id)

        assert storage.check(chat_id=chat_id, user_id=user_id)


class TestMemoryLockStorageUnset:

    def test(self, chat_id, user_id):

        storage = MemoryLockStorage()
        storage.set(chat_id=chat_id, user_id=user_id)
        storage.unset(chat_id=chat_id, user_id=user_id)

        assert not storage.check(chat_id=chat_id, user_id=user_id)


class TestMemoryLockStorageCheck:

    def test(self, chat_id, user_id):

        storage = MemoryLockStorage()
        storage.set(chat_id=chat_id, user_id=user_id)

        assert storage.check(chat_id=chat_id, user_id=user_id)

        storage.unset(chat_id=chat_id, user_id=user_id)

        assert not storage.check(chat_id=chat_id, user_id=user_id)
