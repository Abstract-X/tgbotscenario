import pytest

from tgbotscenario.common.mapping import Mapping
from tgbotscenario import errors


def test():

    mapping = Mapping()

    mapping.add("key", "value")

    value = mapping.get("key")
    assert value == "value"


def test_key_busy():

    mapping = Mapping()
    mapping.add("key", "value")

    with pytest.raises(errors.MappingKeyBusyError):
        mapping.add("key", "another_value")
