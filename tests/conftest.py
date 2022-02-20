import pytest


@pytest.fixture()
def event():
    return object()


@pytest.fixture()
def trigger():
    return lambda event: None
