import pytest

from tgbotscenario.common.scenes.mapping import SceneMapping
from tgbotscenario.common.scenes.base import BaseScene
from tgbotscenario import errors
import tgbotscenario.errors.scene_mapping


class TestSceneMappingAdd:

    def test(self):

        class Scene(BaseScene):
            pass

        mapping = SceneMapping()
        scene = Scene()

        mapping.add(scene)

        assert mapping.get("Scene") is scene

    def test_name_exists(self):

        class FooScene(BaseScene):
            pass

        class BarScene(BaseScene):
            pass

        mapping = SceneMapping()
        foo_scene = FooScene(name="Scene")
        bar_scene = BarScene(name="Scene")
        mapping.add(foo_scene)

        with pytest.raises(errors.scene_mapping.SceneNameBusyError):
            mapping.add(bar_scene)


class TestSceneMappingGet:

    def test(self):

        class Scene(BaseScene):
            pass

        mapping = SceneMapping()
        scene = Scene()
        mapping.add(scene)

        assert mapping.get("Scene") is scene

    def test_name_not_exists(self):

        mapping = SceneMapping()

        with pytest.raises(errors.scene_mapping.SceneNameNotFoundError):
            mapping.get("Scene")
