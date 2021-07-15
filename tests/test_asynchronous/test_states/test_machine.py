import pytest

from tgbotscenario.asynchronous.states.machine import StateMachine
from tgbotscenario.asynchronous.states.storages.memory import MemoryStateStorage
from tgbotscenario.common.states.magazine import StateMagazine


class TestStateMachineInitialState:

    def test(self):

        machine = StateMachine("InitialScene", MemoryStateStorage())

        assert machine.initial_state == "InitialScene"


class TestStateMachineGetCurrentState:

    @pytest.mark.asyncio
    async def test_initialized_machine(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        assert current_state == "InitialScene"

    @pytest.mark.asyncio
    async def test_after_state_change(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        await machine.set_current_state("FooScene", chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        assert current_state == "FooScene"


class TestStateMachineSetCurrentState:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        await machine.set_current_state("FooScene", chat_id=chat_id, user_id=user_id)
        current_state = await machine.get_current_state(chat_id=chat_id, user_id=user_id)

        assert current_state == "FooScene"


class TestStateMachineLoadMagazine:

    @pytest.mark.asyncio
    async def test_initialized_machine(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        magazine = await machine.load_magazine(chat_id=chat_id, user_id=user_id)

        assert magazine == StateMagazine(["InitialScene"])

    @pytest.mark.asyncio
    async def test_after_state_change(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        await machine.set_current_state("FooScene", chat_id=chat_id, user_id=user_id)
        magazine = await machine.load_magazine(chat_id=chat_id, user_id=user_id)

        assert magazine == StateMagazine(["InitialScene", "FooScene"])


class TestStateMachineSaveMagazine:

    @pytest.mark.asyncio
    async def test(self, chat_id, user_id):

        machine = StateMachine("InitialScene", MemoryStateStorage())
        magazine = await machine.load_magazine(chat_id=chat_id, user_id=user_id)
        magazine.set("FooScene")
        await machine.save_magazine(magazine, chat_id=chat_id, user_id=user_id)
        magazine = await machine.load_magazine(chat_id=chat_id, user_id=user_id)

        assert magazine == StateMagazine(["InitialScene", "FooScene"])
