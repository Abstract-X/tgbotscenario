from typing import Optional, Dict, TypeVar

from tgbotscenario import errors


Scene = TypeVar("Scene")
Trigger = TypeVar("Trigger")
Direction = TypeVar("Direction")


class TransitionScheme:

    def __init__(self):
        self._scheme: Dict[
            Scene,  # source scenes
            Dict[
                Trigger,  # triggers
                Dict[
                    Optional[Direction],  # directions
                    Scene  # destination scenes
                ]
            ]
        ] = {}

    def add_transition(self, source_scene: Scene, destination_scene: Scene,
                       trigger: Trigger, direction: Optional[Direction] = None) -> None:
        existing_destination_scene = self._get_destination_scene(source_scene, trigger, direction)
        if existing_destination_scene is destination_scene:
            raise errors.TransitionExistsError(
                "it is not possible to add the transition "
                "(source_scene={source_scene!r}, destination_scene={destination_scene!r}, "
                "trigger={trigger!r}, direction={direction!r}) "
                "because it has already been added earlier!",
                source_scene=source_scene, destination_scene=destination_scene,
                trigger=trigger, direction=direction
            )
        elif existing_destination_scene is not None:
            raise errors.TransitionBusyError(
                "it is not possible to add the transition "
                "(source_scene={source_scene!r}, destination_scene={destination_scene!r}, "
                "trigger={trigger!r}, direction={direction!r}) "
                "because it has already been set to the another "
                "destination scene {existing_destination_scene!r}!",
                source_scene=source_scene, destination_scene=destination_scene, trigger=trigger,
                direction=direction, existing_destination_scene=existing_destination_scene
            )

        self._scheme \
            .setdefault(source_scene, {}) \
            .setdefault(trigger, {})[direction] = destination_scene

    def check_transition(self, source_scene: Scene, destination_scene: Scene,
                         trigger: Trigger, direction: Optional[Direction] = None) -> bool:
        return self._get_destination_scene(source_scene, trigger, direction) is destination_scene

    def check_scene(self, scene: Scene) -> bool:
        for source_scene in self._scheme:
            if source_scene is scene:
                return True
            for trigger in self._scheme[source_scene]:
                for destination_scene in self._scheme[source_scene][trigger].values():
                    if destination_scene is scene:
                        return True

        return False

    def remove_transition(self, source_scene: Scene, trigger: Trigger,
                          direction: Optional[Direction] = None) -> Scene:
        try:
            destination_scene = self._scheme[source_scene][trigger].pop(direction)
        except KeyError:
            raise errors.TransitionForRemovingNotFoundError(
                "it is not possible to remove the transition "
                "(source_scene={source_scene!r}, "
                "trigger={trigger!r}, direction={direction!r}) "
                "because it wasn't added!",
                source_scene=source_scene, trigger=trigger, direction=direction
            ) from None

        if not self._scheme[source_scene][trigger]:
            del self._scheme[source_scene][trigger]
            if not self._scheme[source_scene]:
                del self._scheme[source_scene]

        return destination_scene

    def get_destination_scene(self, source_scene: Scene, trigger: Trigger,
                              direction: Optional[Direction] = None) -> Scene:
        try:
            return self._scheme[source_scene][trigger][direction]
        except KeyError:
            raise errors.DestinationSceneNotFoundError(
                "it is impossible to get the destination scene because the transition "
                "(source_scene={source_scene!r}, "
                "trigger={trigger!r}, direction={direction!r}) "
                "is not set!",
                source_scene=source_scene, trigger=trigger, direction=direction
            ) from None

    def _get_destination_scene(self, source_scene: Scene, trigger: Trigger,
                               direction: Optional[Direction] = None) -> Optional[Scene]:
        try:
            return self._scheme[source_scene][trigger][direction]
        except KeyError:
            return None
