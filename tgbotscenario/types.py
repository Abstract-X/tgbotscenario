from typing import Callable, Dict, Union, Optional

from tgbotscenario.common.scenario.scene_set import SceneSet
from tgbotscenario.asynchronous.scenario.scene import BaseScene as AsyncBaseScene
from tgbotscenario.synchronous.scenario.scene import BaseScene as SyncBaseScene


BaseSceneUnion = Union[AsyncBaseScene, SyncBaseScene]

TransitionDict = Dict[Union[BaseSceneUnion, SceneSet], Dict[Callable, Union[BaseSceneUnion, Dict[str, BaseSceneUnion]]]]
StoredTransitionDict = Dict[BaseSceneUnion, Dict[Callable, Dict[Optional[str], BaseSceneUnion]]]
