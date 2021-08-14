from dataclasses import dataclass

from tgbotscenario.common.mixin import ScenarioMixin
from tgbotscenario.common.scenes.base import BaseScene


class TestScenarioMixinExclude:

    def test(self):

        class InitialScene(BaseScene):
            pass

        class SubScene(BaseScene):
            pass

        @dataclass
        class Scenario(ScenarioMixin):
            initial: InitialScene
            sub: SubScene

        scenario = Scenario(initial=InitialScene(), sub=SubScene())

        assert scenario.exclude(scenario.initial) == {scenario.sub}
        assert scenario.exclude(scenario.sub) == {scenario.initial}
