from tgbotscenario.synchronous.states.storages.memory import MemoryStateStorage


class TestMemoryStateStorageLoad:

    def test_chat_and_user_not_exists(self, chat_id, user_id):

        storage = MemoryStateStorage()
        states = storage.load(chat_id=chat_id, user_id=user_id)

        assert states == []

    def test_chat_and_user_exists(self, chat_id, user_id):

        storage = MemoryStateStorage()
        storage.save(["InitialScene", "FooScene"], chat_id=chat_id, user_id=user_id)
        states = storage.load(chat_id=chat_id, user_id=user_id)

        assert states == ["InitialScene", "FooScene"]

    def test_source_mutability(self, chat_id, user_id):

        storage = MemoryStateStorage()
        source_states = ["InitialScene", "FooScene"]
        storage.save(source_states, chat_id=chat_id, user_id=user_id)
        states = storage.load(chat_id=chat_id, user_id=user_id)
        source_states.clear()

        assert states == ["InitialScene", "FooScene"]


class TestMemoryStateStorageSave:

    def test(self, chat_id, user_id):

        storage = MemoryStateStorage()
        storage.save(["InitialScene", "FooScene"], chat_id=chat_id, user_id=user_id)
        states = storage.load(chat_id=chat_id, user_id=user_id)

        assert states == ["InitialScene", "FooScene"]

    def test_storage_mutability(self, chat_id, user_id):

        storage = MemoryStateStorage()
        source_states = ["InitialScene", "FooScene"]
        storage.save(source_states, chat_id=chat_id, user_id=user_id)
        source_states.clear()
        states = storage.load(chat_id=chat_id, user_id=user_id)

        assert states == ["InitialScene", "FooScene"]
