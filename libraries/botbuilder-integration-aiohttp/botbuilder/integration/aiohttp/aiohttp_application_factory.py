from abc import ABC
from typing import Any

from botbuilder.core.integration import BotApplication, ApplicationFactory

from .aiohttp_bot_application import AioHttpBotApplication
from .aiohttp_bot_apicontroller import AioHttpBotApiController
from .aiohttp_channel_service_exception_middleware import aiohttp_error_middleware


class AioHttpApplicationFactory(ApplicationFactory, ABC):
    def _create_application(self) -> BotApplication:
        return AioHttpBotApplication(self.get_configuration(), middlewares=[aiohttp_error_middleware])

    def _get_default_controller(self) -> Any:
        return AioHttpBotApiController
