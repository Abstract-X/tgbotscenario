from typing import Callable, Dict, Optional, Any

from tgbotscenario.common.scenes.base import BaseScene


TelegramEvent = Any

TransitionSchemeDict = Dict[BaseScene, Dict[Callable, Dict[Optional[str], BaseScene]]]
