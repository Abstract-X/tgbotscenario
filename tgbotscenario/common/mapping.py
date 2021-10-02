from typing import Dict, Any

from tgbotscenario import errors


class Mapping:

    def __init__(self):

        self._mapping: Dict[str, Any] = {}

    def add(self, key: str, value: Any) -> None:

        if key not in self._mapping:
            self._mapping[key] = value
        else:
            existing_value = self.get(key)
            if existing_value is not value:
                raise errors.MappingKeyBusyError(
                    "key {key!r} has already been used to add {value!r} value!",
                    key=key, existing_value=existing_value
                )

    def get(self, key: str) -> Any:

        try:
            return self._mapping[key]
        except KeyError:
            raise errors.MappingKeyNotFoundError("key {key!r} not found!",
                                                 key=key) from None
