import pytest

from tgbotscenario.common.transitions.locks.storage import LockStorage
from tests.generators import generate_chat_id


@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (generate_chat_id(), generate_chat_id()),  # different
        (generate_chat_id(),) * 2  # same
    )
)
def test_lock_not_exists(chat_id, user_id):

    storage = LockStorage()

    assert storage.check_lock(chat_id=chat_id, user_id=user_id) is False


@pytest.mark.parametrize(
    ("chat_id", "user_id"),
    (
        (generate_chat_id(), generate_chat_id()),  # different
        (generate_chat_id(),) * 2  # same
    )
)
def test_lock_exists(chat_id, user_id):

    storage = LockStorage()
    storage.add_lock(chat_id=chat_id, user_id=user_id)

    assert storage.check_lock(chat_id=chat_id, user_id=user_id) is True
