import pytest


@pytest.fixture()
def chat_id():

    return -1001234567890


@pytest.fixture()
def user_id():

    return 1234567890


@pytest.fixture()
def telegram_event_stub():

    return object()


@pytest.fixture()
def scene_data_stub():

    return object()


@pytest.fixture()
def handler_stub():

    async def handler():
        pass

    return handler
