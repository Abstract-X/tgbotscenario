from typing import Optional


class BaseScene:

    def __init__(self, name: Optional[str] = None):
        self._name = name or type(self).__name__

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r})"

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        return self._name
