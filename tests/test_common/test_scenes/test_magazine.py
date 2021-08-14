import pytest

from tgbotscenario.common.scenes.magazine import SceneMagazine
from tgbotscenario.common.scenes.scene import BaseScene
from tgbotscenario import errors
import tgbotscenario.errors.scene_magazine


class TestSceneMagazineInit:

    def test_not_scenes(self):

        with pytest.raises(errors.scene_magazine.SceneMagazineInitializationError):
            SceneMagazine([])


class TestSceneMagazineCurrent:

    def test(self):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        magazine = SceneMagazine([initial_scene, scene])

        assert magazine.current is scene


class TestSceneMagazinePrevious:

    def test_scene_not_exists(self):

        class InitialScene(BaseScene):
            pass

        magazine = SceneMagazine([InitialScene()])

        assert magazine.previous is None

    def test_scene_exists(self):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        magazine = SceneMagazine([initial_scene, scene])

        assert magazine.previous is initial_scene


class TestSceneMagazineSet:

    def test(self):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        magazine = SceneMagazine([initial_scene])

        magazine.set(scene)

        assert magazine == SceneMagazine([initial_scene, scene])

    def test_existing_scene(self):

        class InitialScene(BaseScene):
            pass

        class Scene(BaseScene):
            pass

        initial_scene = InitialScene()
        scene = Scene()
        magazine = SceneMagazine([initial_scene, scene])

        magazine.set(initial_scene)

        assert magazine == SceneMagazine([initial_scene])
