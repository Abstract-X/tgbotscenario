from unittest.mock import AsyncMock

import pytest

from tgbotscenario.asynchronous import BaseScene


@pytest.fixture()
def scene_mock_factory():
    def factory(scene: BaseScene) -> AsyncMock:

        mock = AsyncMock(scene)
        mock.name = scene.name
        mock.process_enter.side_effect = scene.process_enter
        mock.process_exit.side_effect = scene.process_exit

        return mock

    return factory
