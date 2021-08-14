from tgbotscenario.common.locks.storage import LockStorage


class TestLockStorageAdd:

    def test(self, chat_id, user_id):

        storage = LockStorage()

        storage.add(chat_id=chat_id, user_id=user_id)

        assert storage.check(chat_id=chat_id, user_id=user_id)


class TestLockStorageRemove:

    def test(self, chat_id, user_id):

        storage = LockStorage()
        storage.add(chat_id=chat_id, user_id=user_id)

        storage.remove(chat_id=chat_id, user_id=user_id)

        assert not storage.check(chat_id=chat_id, user_id=user_id)

    def test_clearing(self, chat_id, user_id):

        storage = LockStorage()
        foo_user_id = user_id + 1
        bar_user_id = user_id + 2
        storage.add(chat_id=chat_id, user_id=foo_user_id)
        storage.add(chat_id=chat_id, user_id=bar_user_id)

        storage.remove(chat_id=chat_id, user_id=foo_user_id)

        assert chat_id in storage.chat_ids
        assert not storage.check(chat_id=chat_id, user_id=foo_user_id)
        assert storage.check(chat_id=chat_id, user_id=bar_user_id)

        storage.remove(chat_id=chat_id, user_id=bar_user_id)

        assert not storage.check(chat_id=chat_id, user_id=bar_user_id)
        assert chat_id not in storage.chat_ids


class TestLockStorageCheck:

    def test_lock_not_exists(self, chat_id, user_id):

        storage = LockStorage()

        assert storage.check(chat_id=chat_id, user_id=user_id) is False

    def test_lock_exists(self, chat_id, user_id):

        storage = LockStorage()
        storage.add(chat_id=chat_id, user_id=user_id)

        assert storage.check(chat_id=chat_id, user_id=user_id) is True
