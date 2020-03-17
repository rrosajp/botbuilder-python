from abc import abstractmethod, ABC

from botbuilder.core import (
    BotAdapter,
    ActivityHandler,
    BotFrameworkAdapterSettings,
    ConversationState,
    Storage,
)
from .configuration import Configuration
from .default_configuration import DefaultConfiguration
from .bot_adapter_with_errorhandler import AdapterWithErrorHandler
from .bot_controller import BotController
from .bot_application import BotApplication


class ApplicationFactory(ABC):
    def __init__(self):
        self.config = None
        self.application = None
        self.adapter = None
        self.storage = None
        self.conversation_state = None
        self.bot = None

    def get_application(self) -> BotApplication:
        if not self.application:
            self.application = self._create_application()
            self.application.add_post(self._create_controller())
        return self.application

    def get_configuration(self) -> Configuration:
        if not self.config:
            self.config = DefaultConfiguration()
        return self.config

    def get_storage(self) -> Storage:
        if not self.storage:
            self.storage = self._create_storage()
        return self.storage

    def get_conversation_state(self) -> ConversationState:
        if not self.conversation_state:
            self.conversation_state = self._create_conversation_state()
        return self.conversation_state

    def get_adapter_settings(self) -> BotFrameworkAdapterSettings:
        config = self.get_configuration()
        return BotFrameworkAdapterSettings(
            config["MicrosoftAppId"], config["MicrosoftAppPassword"]
        )

    def get_adapter(self) -> BotAdapter:
        if not self.adapter:
            self.adapter = AdapterWithErrorHandler(
                self.get_adapter_settings(), self.get_conversation_state()
            )
        return self.adapter

    def get_bot(self) -> ActivityHandler:
        if not self.bot:
            self.bot = self._create_bot()
        return self.bot

    @abstractmethod
    def _create_application(self) -> BotApplication:
        raise NotImplementedError

    @abstractmethod
    def _create_controller(self) -> BotController:
        raise NotImplementedError()

    @abstractmethod
    def _create_bot(self) -> ActivityHandler:
        raise NotImplementedError()

    def _create_storage(self) -> Storage:
        return None

    def _create_conversation_state(self) -> ConversationState:
        return None
