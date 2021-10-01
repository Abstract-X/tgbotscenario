from typing import Any

from tgbotscenario import errors
import tgbotscenario.errors.magazine


class Magazine:

    def __init__(self, items: list):

        if not items:
            raise errors.magazine.MagazineInitializationError("magazine can't be empty!")

        self._items = items[:]

    def __eq__(self, other):

        return self._items == other

    def __iter__(self):

        return iter(self._items)

    def __repr__(self):

        class_name = type(self).__name__
        return f"<{class_name} {self._items}>"

    @property
    def current(self):

        return self._items[-1]

    @property
    def previous(self):

        try:
            return self._items[-2]
        except IndexError:
            return None

    def set(self, item: Any) -> None:

        try:
            index = self._items.index(item)
        except ValueError:  # item not in magazine
            self._items.append(item)
        else:  # item in magazine
            del self._items[index+1:]
