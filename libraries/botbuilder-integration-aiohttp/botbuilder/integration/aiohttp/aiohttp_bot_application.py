from aiohttp import web
from botbuilder.core.integration import BotApplication, BotController, Configuration
from .aiohttp_bot_controller import AioHttpBotController


class AioHttpBotApplication(BotApplication, web.Application):
    def __init__(self, configuration: Configuration, **kwargs):
        BotApplication.__init__(self, configuration)
        web.Application.__init__(self, **kwargs)

    def run(self, port: int = None, host: str = "localhost"):
        web.run_app(self, host=host or self.config["host"], port=port or self.config["port"])

    def add_post(self, controller: BotController):
        if not isinstance(controller, AioHttpBotController):
            raise TypeError("AioHttpBotController is required")
        self.router.add_post(controller.path(), controller.post)

    def add_get(self, controller: BotController):
        if not isinstance(controller, AioHttpBotController):
            raise TypeError("AioHttpBotController is required")
        self.router.add_get(controller.path(), controller.get)
