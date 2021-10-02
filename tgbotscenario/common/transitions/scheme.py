from typing import Optional, Callable

from tgbotscenario.common.scene import BaseScene
from tgbotscenario.types import TransitionSchemeDict
from tgbotscenario import errors


class TransitionScheme:

    def __init__(self):

        self._scheme: TransitionSchemeDict = {}

    def add_transition(self, source_scene: BaseScene, destination_scene: BaseScene,
                       handler: Callable, direction: Optional[str] = None) -> None:

        existing_destination_scene = self._fetch_destination_scene(source_scene, handler, direction)
        if existing_destination_scene is destination_scene:
            raise errors.TransitionExistsError(
                "transition (source_scene={source_scene!r}, destination_scene={destination_scene!r}, "
                "handler={handler!r}, direction={direction!r}) already exists!", source_scene=source_scene,
                destination_scene=destination_scene, handler=handler, direction=direction
            )
        elif existing_destination_scene is not None:
            raise errors.TransitionBusyError(
                "transition (source_scene={source_scene!r}, destination_scene={destination_scene!r}, "
                "handler={handler!r}, direction={direction!r}) was added earlier for another "
                "destination scene {existing_destination_scene!r}!", source_scene=source_scene,
                destination_scene=destination_scene, handler=handler, direction=direction,
                existing_destination_scene=existing_destination_scene
            )

        self._scheme.setdefault(source_scene, {}).setdefault(handler, {})[direction] = destination_scene

    def check_transition(self, source_scene: BaseScene, destination_scene: BaseScene,
                         handler: Callable, direction: Optional[str] = None) -> bool:

        return self._fetch_destination_scene(source_scene, handler, direction) is destination_scene

    def get_destination_scene(self, source_scene: BaseScene,
                              handler: Callable, direction: Optional[str] = None) -> BaseScene:

        try:
            return self._scheme[source_scene][handler][direction]
        except KeyError:
            raise errors.DestinationSceneNotFoundError(
                "destination scene not found (source_scene={source_scene!r}, handler={handler!r}, "
                "direction={direction!r})!", source_scene=source_scene, handler=handler, direction=direction
            ) from None

    def _fetch_destination_scene(self, source_scene: BaseScene, handler: Callable,
                                 direction: Optional[str] = None) -> Optional[BaseScene]:

        try:
            return self._scheme[source_scene][handler][direction]
        except KeyError:
            return None
