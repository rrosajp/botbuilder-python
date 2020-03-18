from typing import Any, Dict

import tornado.ioloop
import tornado.web
from tornado.options import parse_command_line

from botbuilder.core.integration import BotApplication, Configuration


class TornadoBotApplication(BotApplication):
    def __init__(self, configuration: Configuration):
        BotApplication.__init__(self, configuration)
        self.app = tornado.web.Application()

    def run_bot(self, port: int = None, host: str = "localhost"):
        parse_command_line()
        self.app.listen(port or self.bot_config["port"], host or self.bot_config["host"])
        tornado.ioloop.IOLoop.current().start()

    def add_post(self, path: str, controller: Any, target_kwargs: Dict[str, Any] = None):
        self.app.add_handlers(
            ".*",
            [
                (
                    path,
                    controller,
                    target_kwargs,
                )
            ],
        )

    def add_get(self, path: str, controller: Any, target_kwargs: Dict[str, Any] = None):
        self.app.add_handlers(
            ".*",
            [
                (
                    path,
                    controller,
                    target_kwargs,
                )
            ],
        )
