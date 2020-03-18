from abc import abstractmethod, ABC
from typing import Any, Dict

from .configuration import Configuration


class BotApplication(ABC):
    def __init__(self, configuration: Configuration):
        self.config = configuration

    @abstractmethod
    def run(self, port: int = None, host: str = "localhost"):
        """
        Runs the application.
        :param port: [Optional] Defaults to "port" in Configuration
        :param host: [Optional] Defaults to "localhost" or "host" in Configuration
        """
        raise NotImplementedError()

    @abstractmethod
    def add_post(self, path: str, controller: Any, target_kwargs: Dict[str, Any] = None):
        """
        Adds a POST handler
        :param path: The URL the handler will respond to
        :param controller: The class name of the controller
        :param target_kwargs: Required arguments for the BotController.  MUST include 'adapter' and 'bot'.
        """
        raise NotImplementedError()

    @abstractmethod
    def add_get(self, path: str, controller: Any, target_kwargs: Dict[str, Any] = None):
        """
        Adds a GET handler
        :param path: The URL the handler will respond to
        :param controller: The class name of the controller
        :param target_kwargs: Required arguments for the BotController.  MUST include 'adapter' and 'bot'.
        """
        raise NotImplementedError()
