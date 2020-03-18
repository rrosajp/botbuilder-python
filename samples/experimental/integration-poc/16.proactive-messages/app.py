# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import uuid
from abc import ABC
from http import HTTPStatus
from typing import Dict

from botbuilder.core import ActivityHandler
from botbuilder.integration.tornado import TornadoBotController, TornadoApplicationFactory
from botbuilder.schema import ConversationReference
from tornado import httputil
from tornado.web import Application

from bots import ProactiveBot


# Create a shared dictionary.  The Bot will add conversation references when users
# join the conversation and send messages.
CONVERSATION_REFERENCES: Dict[str, ConversationReference] = dict()


class BotApplicationFactory(TornadoApplicationFactory):
    def _create_bot(self) -> ActivityHandler:
        return ProactiveBot(CONVERSATION_REFERENCES)


class NotifyBotController(TornadoBotController, ABC):
    """
    Handles proactive messages sent to /api/notify

    Technically this doesn't have to derive from TornadoBotController.  It could
    implement a typical Tornado RequestHandler.
    """
    def __init__(
            self, application: "Application", request: httputil.HTTPServerRequest, **kwargs
    ):
        TornadoBotController.__init__(self, application, request, **kwargs)

        # If the channel is the Emulator, and authentication is not in use, the AppId will be null.
        # We generate a random AppId for this case only. This is not required for production, since
        # the AppId will have a value.
        self.config = kwargs["configuration"]
        self.app_id = self.config["MicrosoftAppId"] or uuid.uuid4()

    async def get(self):
        for conversation_reference in CONVERSATION_REFERENCES.values():
            await self.adapter.continue_conversation(
                conversation_reference,
                lambda turn_context: turn_context.send_activity("proactive hello"),
                self.app_id,
            )

        self.write("Proactive messages have been sent")
        self.set_status(HTTPStatus.OK)


APP_FACTORY = BotApplicationFactory()
APP = APP_FACTORY.get_application()
APP.add_get(
    "/api/notify",
    NotifyBotController,
    {
        "adapter": APP_FACTORY.get_adapter(),
        "bot": APP_FACTORY.get_bot(),
        "configuration": APP_FACTORY.get_configuration(),
    },
)

if __name__ == "__main__":
    APP.run()
