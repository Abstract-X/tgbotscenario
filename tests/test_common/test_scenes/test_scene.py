from tgbotscenario.common.scenes.scene import BaseScene


class TestBaseSceneName:

    def test(self):

        class Scene(BaseScene):
            pass

        foo_scene = Scene()

        assert foo_scene.name == "Scene"

    def test_another_name(self):

        class Scene(BaseScene):
            pass

        foo_scene = Scene(name="AnotherScene")

        assert foo_scene.name == "AnotherScene"
