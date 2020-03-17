# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botbuilder.core import ActivityHandler
from botbuilder.integration.aiohttp import AioHttpApplicationFactory

from bots import EchoBot


class EchoApplicationFactory(AioHttpApplicationFactory):
    def _create_bot(self) -> ActivityHandler:
        return EchoBot()


APP = EchoApplicationFactory().get_application()

if __name__ == "__main__":
    APP.run()
