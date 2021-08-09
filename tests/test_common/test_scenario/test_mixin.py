from dataclasses import dataclass

from tgbotscenario.common.scenario.mixin import ScenarioMixin
from tgbotscenario.asynchronous.scenario.scene import BaseScene


class TestBaseScenarioExclude:

    def test_scenes_not_exists(self):

        @dataclass
        class Scenario(ScenarioMixin):
            pass

        scenario = Scenario()

        assert scenario.exclude() == set()

    def test_scenes_exists(self):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()

        @dataclass
        class Scenario(ScenarioMixin):
            initial: InitialScene
            foo: FooScene

        scenario = Scenario(
            initial=initial_scene,
            foo=foo_scene
        )

        assert scenario.exclude() == {initial_scene, foo_scene}

    def test_with_exclude(self):

        class InitialScene(BaseScene):
            pass

        class FooScene(BaseScene):
            pass

        initial_scene = InitialScene()
        foo_scene = FooScene()

        @dataclass
        class Scenario(ScenarioMixin):
            initial: InitialScene
            foo: FooScene

        scenario = Scenario(
            initial=initial_scene,
            foo=foo_scene
        )

        assert scenario.exclude(scenario.initial) == {foo_scene}
        assert scenario.exclude(scenario.foo) == {initial_scene}
