from unittest.mock import MagicMock

from tgbotscenario.synchronous.scenario.locks.context import LockContext


class TestLockContextEnter:

    def test(self, chat_id, user_id):

        storage_mock = MagicMock()
        with LockContext(storage_mock, chat_id=chat_id, user_id=user_id):
            pass

        storage_mock.add.assert_called_once_with(chat_id=chat_id, user_id=user_id)


class TestLockContextExit:

    def test(self, chat_id, user_id):

        storage_mock = MagicMock()
        with LockContext(storage_mock, chat_id=chat_id, user_id=user_id):
            pass

        storage_mock.remove.assert_called_once_with(chat_id=chat_id, user_id=user_id)
