import pytest

from tgbotscenario.common.states.magazine import StateMagazine
from tgbotscenario import errors
import tgbotscenario.errors.state_magazine


class TestStateMagazineInit:

    def test_pass_empty_states(self):

        with pytest.raises(errors.state_magazine.StateMagazineInitializationError):
            StateMagazine([])


class TestStateMagazineCurrent:

    def test(self):

        magazine = StateMagazine(["InitialScene", "FooScene"])

        assert magazine.current == "FooScene"


class TestStateMagazinePrevious:

    def test_previous_state_not_exists(self):

        magazine = StateMagazine(["InitialScene"])

        assert magazine.previous is None

    def test_previous_state_exists(self):

        magazine = StateMagazine(["InitialScene", "FooScene"])

        assert magazine.previous == "InitialScene"


class TestStateMagazineSet:

    def test_state_not_exists(self):

        magazine = StateMagazine(["InitialScene"])
        magazine.set("FooScene")

        assert list(magazine) == ["InitialScene", "FooScene"]
        assert magazine.current == "FooScene"

    def test_state_exists(self):

        magazine = StateMagazine(["InitialScene", "FooScene", "BarScene"])
        magazine.set("FooScene")

        assert list(magazine) == ["InitialScene", "FooScene"]
        assert magazine.current == "FooScene"
