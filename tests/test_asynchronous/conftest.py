from unittest.mock import AsyncMock

import pytest

from tgbotscenario.asynchronous.scenes.base import BaseScene
from tgbotscenario.asynchronous.scenes.storages.base import AbstractSceneStorage


@pytest.fixture()
def scene_mock_factory():
    def factory(scene: BaseScene) -> AsyncMock:

        mock = AsyncMock(scene)
        mock.name = scene.name
        mock.process_enter.side_effect = scene.process_enter
        mock.process_exit.side_effect = scene.process_exit

        return mock

    return factory


@pytest.fixture()
def scene_storage_mock_factory():
    def factory(storage: AbstractSceneStorage) -> AsyncMock:

        mock = AsyncMock(storage)
        mock.load.side_effect = storage.load
        mock.save.side_effect = storage.save

        return mock

    return factory
