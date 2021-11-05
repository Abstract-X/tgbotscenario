from dataclasses import dataclass

from tgbotscenario.common.scene import BaseScene
from tgbotscenario.common.scenario import BaseScenario


def test():

    class FooScene(BaseScene):
        pass

    class BarScene(BaseScene):
        pass

    @dataclass
    class Scenario(BaseScenario):
        foo: BaseScene
        bar: BaseScene

    scenario = Scenario(foo=FooScene(), bar=BarScene())

    scenes = scenario.select(exclude={scenario.foo})

    assert scenes == {scenario.bar}
