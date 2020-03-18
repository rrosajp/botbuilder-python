from abc import ABC
from typing import Any

from botbuilder.core.integration import BotApplication, ApplicationFactory

from .quart_bot_application import QuartBotApplication
from .quart_bot_apicontroller import QuartBotApiController


class QuartApplicationFactory(ApplicationFactory, ABC):
    def _create_application(self) -> BotApplication:
        return QuartBotApplication("bot", self.get_configuration())

    def _get_default_controller(self) -> Any:
        return QuartBotApiController
