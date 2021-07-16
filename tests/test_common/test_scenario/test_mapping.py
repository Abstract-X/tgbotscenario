import pytest

from tgbotscenario.asynchronous.scenario.scene import BaseScene
from tgbotscenario.common.scenario.mapping import SceneMapping
from tgbotscenario import errors
import tgbotscenario.errors.scene_mapping


class TestSceneMappingScenes:

    def test(self):

        class FooScene(BaseScene):
            pass

        class BarScene(BaseScene):
            pass

        foo_scene = FooScene()
        bar_scene = BarScene()
        mapping = SceneMapping((foo_scene, bar_scene))

        assert mapping.scenes == {foo_scene, bar_scene}


class TestSceneMappingAdd:

    def test(self):

        class FooScene(BaseScene):
            pass

        mapping = SceneMapping()
        foo_scene = FooScene()
        mapping.add(foo_scene)

        assert mapping.get("FooScene") is foo_scene

    def test_scene_name_exists_with_another_scene(self):

        class FooScene(BaseScene):
            pass

        class BarScene(BaseScene):
            pass

        foo_scene = FooScene()
        bar_scene = BarScene("FooScene")
        mapping = SceneMapping((foo_scene,))

        with pytest.raises(errors.scene_mapping.SceneNameBusyError):
            mapping.add(bar_scene)


class TestSceneMappingRemove:

    def test(self):

        class FooScene(BaseScene):
            pass

        foo_scene = FooScene()
        mapping = SceneMapping((foo_scene,))
        mapping.remove("FooScene")

        with pytest.raises(errors.scene_mapping.SceneNameNotFoundError):
            mapping.get("FooScene")

    def test_name_not_exists(self):

        mapping = SceneMapping()

        with pytest.raises(errors.scene_mapping.SceneNameNotFoundError):
            mapping.remove("FooScene")


class TestSceneMappingGet:

    def test(self):

        class FooScene(BaseScene):
            pass

        foo_scene = FooScene()
        mapping = SceneMapping((foo_scene,))

        assert mapping.get("FooScene") is foo_scene

    def test_name_not_exists(self):

        mapping = SceneMapping()

        with pytest.raises(errors.scene_mapping.SceneNameNotFoundError):
            mapping.get("FooScene")
