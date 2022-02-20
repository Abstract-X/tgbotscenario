from dataclasses import dataclass

from tgbotscenario.asynchronous import Scene
from tgbotscenario.common import BaseScenario


def test_behavior():
    @dataclass
    class Scenario(BaseScenario):
        foo: Scene

    foo_scene = Scene("FooScene")
    bar_scene = Scene("BarScene")
    scenario = Scenario(foo=foo_scene)

    assert foo_scene in scenario
    assert bar_scene not in scenario
