from typing import Dict, TypeVar

from tgbotscenario import errors


Value = TypeVar("Value")


class Mapping:

    def __init__(self):
        self._keys_values: Dict[str, Value] = {}
        self._values_keys: Dict[Value, str] = {}

    def add(self, key: str, value: Value) -> None:
        if key in self._keys_values:
            existing_value = self.get_value(key)
            if existing_value != value:
                raise errors.MappingKeyBusyError(
                    "it is not possible to add the {value!r} value because the {key!r} key "
                    "has already been used for the {existing_value!r} value!",
                    key=key, value=value, existing_value=existing_value
                )
        if value in self._values_keys:
            existing_key = self.get_key(value)
            if existing_key != key:
                raise errors.MappingValueBusyError(
                    "it is not possible to add the {value!r} value with the {key!r} key "
                    "because it was added earlier with the {existing_key!r} key!",
                    value=value, key=key, existing_key=existing_key
                )

        self._keys_values[key] = value
        self._values_keys[value] = key

    def remove(self, key: str, value: Value) -> None:
        try:
            del self._keys_values[key]
        except KeyError:
            raise errors.MappingDataNotFoundError(
                "it is not possible to remove the {key!r} key and "
                "the {value!r} value because they were not added!",
                key=key, value=value
            ) from None

        del self._values_keys[value]

    def get_key(self, value: Value) -> str:
        try:
            return self._values_keys[value]
        except KeyError:
            raise errors.MappingValueNotFoundError(
                "it is not possible to get a key for the {value!} value "
                "because it hasn't been added!",
                value=value
            ) from None

    def get_value(self, key: str) -> Value:
        try:
            return self._keys_values[key]
        except KeyError:
            raise errors.MappingKeyNotFoundError(
                "it is not possible to get the value for the {key!r} key "
                "because it hasn't been added!",
                key=key
            ) from None
