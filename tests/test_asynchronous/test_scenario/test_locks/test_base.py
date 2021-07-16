from unittest.mock import AsyncMock

import pytest

from tgbotscenario.asynchronous.scenario.locks.base import LockContext


class TestLockContextAenter:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id):

        storage_mock = AsyncMock()
        async with LockContext(storage_mock, chat_id=chat_id, user_id=user_id):
            pass

        storage_mock.add.assert_awaited_once_with(chat_id=chat_id, user_id=user_id)


class TestLockContextAexit:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id):

        storage_mock = AsyncMock()
        async with LockContext(storage_mock, chat_id=chat_id, user_id=user_id):
            pass

        storage_mock.remove.assert_awaited_once_with(chat_id=chat_id, user_id=user_id)
