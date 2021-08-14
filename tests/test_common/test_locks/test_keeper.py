import pytest

from tgbotscenario.common.locks.keeper import LockKeeper
from tgbotscenario import errors
import tgbotscenario.errors.lock_keeper


class TestLockKeeperAcquire:

    def test(self, chat_id, user_id):

        lock_keeper = LockKeeper()

        with lock_keeper.acquire(chat_id=chat_id, user_id=user_id):
            assert lock_keeper.check(chat_id=chat_id, user_id=user_id)

        assert not lock_keeper.check(chat_id=chat_id, user_id=user_id)

    def test_lock_exists(self, chat_id, user_id):

        lock_keeper = LockKeeper()

        with lock_keeper.acquire(chat_id=chat_id, user_id=user_id):
            with pytest.raises(errors.lock_keeper.TransitionLockExistsError):
                with lock_keeper.acquire(chat_id=chat_id, user_id=user_id):
                    pass


class TestLockKeeperCheck:

    def test_lock_not_exists(self, chat_id, user_id):

        lock_keeper = LockKeeper()

        assert lock_keeper.check(chat_id=chat_id, user_id=user_id) is False

    def test_lock_exists(self, chat_id, user_id):

        lock_keeper = LockKeeper()

        with lock_keeper.acquire(chat_id=chat_id, user_id=user_id):
            assert lock_keeper.check(chat_id=chat_id, user_id=user_id) is True
