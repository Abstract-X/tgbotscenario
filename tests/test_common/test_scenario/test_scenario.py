from tgbotscenario.common.scenario.scenario import BaseScenario
from tgbotscenario.asynchronous.scenario.scene import BaseScene


class TestBaseScenarioSelect:

    def test_scenes_not_exists(self):

        class Scenario(BaseScenario):
            pass

        scenario = Scenario()

        assert scenario.select() == set()

    def test_scenes_exists(self):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()

        class Scenario(BaseScenario):
            INITIAL = initial_scene
            FOO = foo_scene

        scenario = Scenario()

        assert scenario.select() == {initial_scene, foo_scene}

    def test_with_exclude(self):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()

        class Scenario(BaseScenario):
            INITIAL = initial_scene
            FOO = foo_scene

        scenario = Scenario()

        assert scenario.select(exclude=initial_scene) == {foo_scene}
        assert scenario.select(exclude=(initial_scene,)) == {foo_scene}
