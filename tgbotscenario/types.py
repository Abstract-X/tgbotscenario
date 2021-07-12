from typing import Callable, Dict, Union, Optional

from tgbotscenario.common.scenario.scene_set import SceneSet
from tgbotscenario.asynchronous.scenario.scene import AbstractScene as AsyncAbstractScene
from tgbotscenario.synchronous.scenario.scene import AbstractScene as SyncAbstractScene


AbstractSceneUnion = Union[AsyncAbstractScene, SyncAbstractScene]

TransitionDict = (Dict[Union[AbstractSceneUnion, SceneSet],
                       Dict[Callable, Union[AbstractSceneUnion, Dict[str, AbstractSceneUnion]]]])
StoredTransitionDict = Dict[AbstractSceneUnion, Dict[Callable, Dict[Optional[str], AbstractSceneUnion]]]
