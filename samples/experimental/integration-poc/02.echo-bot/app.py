# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botbuilder.core import ActivityHandler
from botbuilder.integration.aiohttp import AioHttpApplicationFactory

from bots import EchoBot


# Subclass ApplicationFactory so that a Bot can be created.
class BotApplicationFactory(AioHttpApplicationFactory):
    def _create_bot(self) -> ActivityHandler:
        # EchoBot is our bot in this project.
        return EchoBot()


# Create the BotApplication.  The ARM templates expect that
# that the application is in the variable 'APP'
APP = BotApplicationFactory().get_application()

if __name__ == "__main__":
    APP.run()
