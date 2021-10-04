import pytest

from tgbotscenario.common.mapping import Mapping
from tgbotscenario import errors


def test():

    mapping = Mapping()
    mapping.add("key", "value")

    value = mapping.get("key")

    assert value == "value"


def test_key_not_found():

    mapping = Mapping()

    with pytest.raises(errors.MappingKeyNotFoundError):
        mapping.get("unknown_key")
