from abc import ABC
from typing import Any

from botbuilder.core.integration import BotApplication, ApplicationFactory

from .tornado_bot_application import TornadoBotApplication
from .tornado_bot_apicontroller import TornadoBotApiController


class TornadoApplicationFactory(ApplicationFactory, ABC):
    def _create_application(self) -> BotApplication:
        return TornadoBotApplication(self.get_configuration())

    def _get_default_controller(self) -> Any:
        return TornadoBotApiController
