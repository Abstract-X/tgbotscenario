import pytest

from tgbotscenario.asynchronous import Scene


class TestScene(Scene):
    pass


@pytest.mark.parametrize(
    ("name", "expected_name"),
    (
        (None, "TestScene"),
        ("FooScene", "FooScene")
    )
)
def test_behavior(name, expected_name):
    scene = TestScene(name)

    assert scene.name == expected_name
