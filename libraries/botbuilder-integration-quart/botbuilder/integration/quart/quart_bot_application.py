from typing import Any, Dict

from botbuilder.core.integration import BotApplication, Configuration
from quart import Quart


class QuartBotApplication(BotApplication, Quart):
    def __init__(self, name: str, configuration: Configuration):
        BotApplication.__init__(self, configuration)
        Quart.__init__(self, name)

        self.config.from_mapping(self.bot_config.all())

    def run_bot(self, port: int = None, host: str = "localhost"):
        self.run(
            debug=False, port=port or self.bot_config["port"]
        )

    def add_post(
        self, path: str, controller: Any, target_kwargs: Dict[str, Any] = None
    ):
        controller_instance = controller(**target_kwargs)
        self.add_url_rule(path, methods=["POST"], view_func=controller_instance.messages)

    def add_get(self, path: str, controller: Any, target_kwargs: Dict[str, Any] = None):
        controller_instance = controller(**target_kwargs)
        self.add_url_rule(path, methods=["GET"], view_func=controller_instance.messages)
