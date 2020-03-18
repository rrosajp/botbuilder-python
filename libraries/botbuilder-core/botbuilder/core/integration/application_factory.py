from abc import abstractmethod, ABC
from typing import Any

from botbuilder.core import (
    BotAdapter,
    ActivityHandler,
    BotFrameworkAdapterSettings,
    ConversationState,
    Storage,
)
from .configuration import Configuration
from .configparser_configuration import ConfigParserConfiguration
from .bot_adapter_with_errorhandler import AdapterWithErrorHandler
from .bot_application import BotApplication


class ApplicationFactory(ABC):
    """
    This provides BotApplication and Bot object creation.  This class will wire up a bot
    application with the objects required to run.

    The default object types are:
    Configuration = DefaultConfiguration
    BotFrameworkAdapterSettings = A class using MicrosoftAppId and MicrosoftPassword from Configuration
    BotAdapter = BotFrameworkAdapter
    Storage = None
    ConversationState = None

    This class MUST be subclassed, and an implementation for '_create_bot' provided.

    If a different BotAdapter, Storage, Configuration, ConversationState is
    required, the subclass can override the appropriate "_create_*" method.  In all cases, the
    "get_*" methods should be used to access objects.
    """

    def __init__(self):
        self.__config = None
        self.__application = None
        self.__adapter = None
        self.__storage = None
        self.__conversation_state = None
        self.__bot = None

    def get_application(self) -> BotApplication:
        """
        Gets a BotApplication object.

        The returned object can be used to add new BotControllers which handle specific URL's.
        This method will automatically add a BotController to handle /api/messages for the Bot.

        After adding any additional BotControllers, "BotApplication.run" should be called to
        start the app and respond to incoming requests.

        :return: A BotApplication
        """
        if not self.__application:
            self.__application = self._create_application()
            self.__application.add_post(
                "/api/messages",
                self._get_default_controller(),
                dict(adapter=self.get_adapter(), bot=self.get_bot()),
            )
        return self.__application

    def get_configuration(self) -> Configuration:
        if not self.__config:
            self.__config = ConfigParserConfiguration()
        return self.__config

    def get_storage(self) -> Storage:
        if not self.__storage:
            self.__storage = self._create_storage()
        return self.__storage

    def get_conversation_state(self) -> ConversationState:
        if not self.__conversation_state:
            self.__conversation_state = self._create_conversation_state()
        return self.__conversation_state

    def get_adapter_settings(self) -> BotFrameworkAdapterSettings:
        config = self.get_configuration()
        return BotFrameworkAdapterSettings(
            config["MicrosoftAppId"], config["MicrosoftAppPassword"]
        )

    def get_adapter(self) -> BotAdapter:
        if not self.__adapter:
            self.__adapter = AdapterWithErrorHandler(
                self.get_adapter_settings(), self.get_conversation_state()
            )
        return self.__adapter

    def get_bot(self) -> ActivityHandler:
        if not self.__bot:
            self.__bot = self._create_bot()
        return self.__bot

    @abstractmethod
    def _create_application(self) -> BotApplication:
        raise NotImplementedError

    @abstractmethod
    def _get_default_controller(self) -> Any:
        """
        Creates the default Bot API controller (/api/messages).  Subclasses must implement
        this to return a web framework appropriate POST handler.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def _create_bot(self) -> ActivityHandler:
        raise NotImplementedError()

    def _create_storage(self) -> Storage:
        return None

    def _create_conversation_state(self) -> ConversationState:
        storage = self.get_storage()
        if storage:
            return ConversationState(storage)
        return None
