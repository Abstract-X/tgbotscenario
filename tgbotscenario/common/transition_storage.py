from typing import Optional, Callable

from tgbotscenario.types import StoredTransitionDict, BaseSceneUnion
from tgbotscenario import errors
import tgbotscenario.errors.transition_storage


class TransitionStorage:

    def __init__(self):

        self._storage: StoredTransitionDict = {}

    def add(self, source_scene: BaseSceneUnion, destination_scene: BaseSceneUnion,
            handler: Callable, direction: Optional[str] = None) -> None:

        existing_destination_scene = self._fetch_destination_scene(source_scene, handler, direction)
        if existing_destination_scene is destination_scene:
            raise errors.transition_storage.TransitionExistsError(
                "transition (source_scene={source_scene!r}, destination_scene={destination_scene!r}, "
                "handler={handler!r}, direction={direction!r}) already exists!", source_scene=source_scene,
                destination_scene=destination_scene, handler=handler, direction=direction
            )
        elif existing_destination_scene is not None:
            raise errors.transition_storage.TransitionBusyError(
                "transition (source_scene={source_scene!r}, destination_scene={destination_scene!r}, "
                "handler={handler!r}, direction={direction!r}) was added earlier for another "
                "destination scene {existing_destination_scene!r}!", source_scene=source_scene,
                destination_scene=destination_scene, handler=handler, direction=direction,
                existing_destination_scene=existing_destination_scene
            )

        if source_scene not in self._storage:
            self._storage[source_scene] = {}
        if handler not in self._storage[source_scene]:
            self._storage[source_scene][handler] = {}

        self._storage[source_scene][handler][direction] = destination_scene

    def check(self, source_scene: BaseSceneUnion, destination_scene: BaseSceneUnion,
              handler: Callable, direction: Optional[str] = None) -> bool:

        return self._fetch_destination_scene(source_scene, handler, direction) is destination_scene

    def remove(self, source_scene: BaseSceneUnion, handler: Callable,
               direction: Optional[str] = None) -> BaseSceneUnion:

        try:
            destination_scene = self._storage[source_scene][handler].pop(direction)
        except KeyError:
            raise errors.transition_storage.TransitionForRemovingNotFoundError(
                "transition not found (source_scene={source_scene!r}, handler={handler!r}, direction={direction!r})!",
                source_scene=source_scene, handler=handler, direction=direction
            ) from None

        if not self._storage[source_scene][handler]:
            del self._storage[source_scene][handler]
        if not self._storage[source_scene]:
            del self._storage[source_scene]

        return destination_scene

    def get_destination_scene(self, source_scene: BaseSceneUnion,
                              handler: Callable, direction: Optional[str] = None) -> BaseSceneUnion:

        try:
            return self._storage[source_scene][handler][direction]
        except KeyError:
            raise errors.transition_storage.DestinationSceneNotFoundError(
                "destination scene not found (source_scene={source_scene!r}, handler={handler!r}, "
                "direction={direction!r})!", source_scene=source_scene, handler=handler, direction=direction
            ) from None

    def _fetch_destination_scene(self, source_scene: BaseSceneUnion, handler: Callable,
                                 direction: Optional[str] = None) -> Optional[BaseSceneUnion]:

        try:
            return self._storage[source_scene][handler][direction]
        except KeyError:
            return None
