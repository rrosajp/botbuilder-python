from abc import abstractmethod, ABC

from .configuration import Configuration
from .bot_controller import BotController


class BotApplication(ABC):
    def __init__(self, configuration: Configuration):
        self.config = configuration

    @abstractmethod
    def run(self, port: int = None, host: str = "localhost"):
        raise NotImplementedError()

    @abstractmethod
    def add_post(self, controller: BotController):
        raise NotImplementedError()

    @abstractmethod
    def add_get(self, controller: BotController):
        raise NotImplementedError()
