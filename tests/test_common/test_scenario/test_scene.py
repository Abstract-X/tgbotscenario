from tgbotscenario.common.scenario.scene import BaseScene


class TestBaseSceneName:

    def test_get(self):

        class FooScene(BaseScene):
            pass

        foo_scene = FooScene()

        assert foo_scene.name == "FooScene"

    def test_set(self):

        class FooScene(BaseScene):
            pass

        foo_scene = FooScene("BarScene")

        assert foo_scene.name == "BarScene"
