from dataclasses import dataclass

from tgbotscenario.asynchronous import Scene
from tgbotscenario.common import BaseScenario


def test_behavior():
    @dataclass
    class Scenario(BaseScenario):
        foo: Scene
        bar: Scene

    scenario = Scenario(foo=Scene("FooScene"), bar=Scene("BarScene"))

    assert len(scenario) == 2
