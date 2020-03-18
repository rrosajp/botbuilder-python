from typing import Any, Dict

from aiohttp import web
from botbuilder.core.integration import BotApplication, BotController, Configuration


class AioHttpBotApplication(BotApplication, web.Application):
    def __init__(self, configuration: Configuration, **kwargs):
        BotApplication.__init__(self, configuration)
        web.Application.__init__(self, **kwargs)

    def run(self, port: int = None, host: str = "localhost"):
        web.run_app(
            self, host=host or self.config["host"], port=port or self.config["port"]
        )

    def add_post(
        self, path: str, controller: Any, target_kwargs: Dict[str, Any] = None
    ):
        controller_instance = controller(**target_kwargs)
        self.router.add_post(path, controller_instance.post)

    def add_get(self, path: str, controller: Any, target_kwargs: Dict[str, Any] = None):
        controller_instance = controller(**target_kwargs)
        self.router.add_get(path, controller_instance.get)
