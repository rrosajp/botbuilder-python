# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows how to create a bot that demonstrates the following:
- Use [LUIS](https://www.luis.ai) to implement core AI capabilities.
- Implement a multi-turn conversation using Dialogs.
- Handle user interruptions for such things as `Help` or `Cancel`.
- Prompt for and validate requests for information from the user.
"""

from botbuilder.core import MemoryStorage, UserState, ActivityHandler, Storage
from botbuilder.integration.aiohttp import AioHttpApplicationFactory

from dialogs import MainDialog, BookingDialog
from bots import DialogAndWelcomeBot
from flight_booking_recognizer import FlightBookingRecognizer


class BotApplicationFactory(AioHttpApplicationFactory):
    def _create_storage(self) -> Storage:
        return MemoryStorage()

    def _create_bot(self) -> ActivityHandler:
        recognizer = FlightBookingRecognizer(self.get_configuration())
        booking_dialog = BookingDialog()
        dialog = MainDialog(recognizer, booking_dialog)
        user_state = UserState(self.get_storage())

        bot = DialogAndWelcomeBot(self.get_conversation_state(), user_state, dialog)
        return bot


APP = BotApplicationFactory().get_application()

if __name__ == "__main__":
    APP.run()
