from typing import List, Optional, TypeVar

from tgbotscenario import errors


Item = TypeVar("Item")


class Magazine:

    def __init__(self, items: List[Item]):
        if not items:
            raise errors.MagazineInitializationError(
                "magazine can't be empty!"
            )
        self._items = items[:]

    def __eq__(self, other):
        return self._items == other

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return f"{type(self).__name__}({self._items!r})"

    @property
    def current(self) -> Item:
        return self._items[-1]

    @property
    def previous(self) -> Optional[Item]:
        try:
            return self._items[-2]
        except IndexError:
            return None

    def set(self, item: Item) -> None:
        try:
            index = self._items.index(item)
        except ValueError:
            self._items.append(item)
        else:
            del self._items[index+1:]
