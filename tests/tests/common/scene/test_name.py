from tgbotscenario.common.scene import BaseScene


def test_default_name():

    class SomeScene(BaseScene):
        pass

    scene = SomeScene()

    assert scene.name == "SomeScene"


def test_passed_name():

    class Scene(BaseScene):
        pass

    scene = Scene("TestScene")

    assert scene.name == "TestScene"
