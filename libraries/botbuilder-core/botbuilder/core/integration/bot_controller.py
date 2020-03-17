from abc import abstractmethod, ABC

from botbuilder.core import BotAdapter, ActivityHandler


class BotController(ABC):
    def __init__(self, adapter: BotAdapter, bot: ActivityHandler):
        self.adapter = adapter
        self.bot = bot

    @abstractmethod
    def path(self) -> str:
        raise NotImplementedError()
