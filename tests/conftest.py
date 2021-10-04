import pytest

from tests.generators import generate_chat_id


@pytest.fixture()
def chat_id():

    return generate_chat_id()


@pytest.fixture()
def user_id():

    return generate_chat_id()


@pytest.fixture()
def event():

    return object()


@pytest.fixture()
def handler():

    return lambda event: None
