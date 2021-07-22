from tgbotscenario.synchronous.states.machine import StateMachine
from tgbotscenario.synchronous.states.storages.memory import MemoryStateStorage
from tgbotscenario.common.states.magazine import StateMagazine


class TestStateMachineInitialState:

    def test(self):

        machine = StateMachine("InitialScene", MemoryStateStorage())

        assert machine.initial_state == "InitialScene"


class TestStateMachineGetCurrentState:

    def test_initialized_machine(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        assert current_state == "InitialScene"

    def test_after_state_change(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        machine.set_current_state("FooScene", chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        assert current_state == "FooScene"


class TestStateMachineSetCurrentState:

    def test(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        machine.set_current_state("FooScene", chat_id=chat_id, user_id=user_id)
        current_state = machine.get_current_state(chat_id=chat_id, user_id=user_id)

        assert current_state == "FooScene"


class TestStateMachineLoadMagazine:

    def test_initialized_machine(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        magazine = machine.load_magazine(chat_id=chat_id, user_id=user_id)

        assert magazine == StateMagazine(["InitialScene"])

    def test_after_state_change(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        machine.set_current_state("FooScene", chat_id=chat_id, user_id=user_id)
        magazine = machine.load_magazine(chat_id=chat_id, user_id=user_id)

        assert magazine == StateMagazine(["InitialScene", "FooScene"])


class TestStateMachineSaveMagazine:

    def test(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        magazine = machine.load_magazine(chat_id=chat_id, user_id=user_id)
        magazine.set("FooScene")
        machine.save_magazine(magazine, chat_id=chat_id, user_id=user_id)
        magazine = machine.load_magazine(chat_id=chat_id, user_id=user_id)

        assert magazine == StateMagazine(["InitialScene", "FooScene"])
