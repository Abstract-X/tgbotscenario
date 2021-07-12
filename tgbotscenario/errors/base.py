from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class BaseError(Exception):

    raw_message: str

    def __post_init__(self):

        self._format_kwargs = self._get_format_kwargs()

    def __str__(self):

        return self.message

    @property
    def message(self) -> str:

        return self.raw_message.format(**self._format_kwargs)

    def _get_format_kwargs(self) -> Dict[str, Any]:

        kwargs = vars(self).copy()
        del kwargs["raw_message"]  # removing base attributes

        return kwargs
