import sys
import traceback
from datetime import datetime

from botbuilder.core import BotFrameworkAdapter, TurnContext, BotFrameworkAdapterSettings, ConversationState
from botbuilder.schema import Activity, ActivityTypes


class AdapterWithErrorHandler(BotFrameworkAdapter):
    """
    A BotFrameworkAdapter that provides a default implementation of error handling in
    a bot.  In a production Bot, this handler is probably not what you'd want and a
    custom error handler should be provided.
    """

    def __init__(self, settings: BotFrameworkAdapterSettings, conversation_state: ConversationState = None):
        super().__init__(settings)
        self.on_error = AdapterWithErrorHandler.on_bot_error
        self.conversation_state = conversation_state

    # Catch-all for errors.
    async def on_bot_error(self, context: TurnContext, error: Exception):
        # This check writes out errors to console log .vs. app insights.
        # NOTE: In production environment, you should consider logging this to Azure
        #       application insights.
        print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
        traceback.print_exc()

        # Send a message to the user
        await context.send_activity("The bot encountered an error or bug.")
        await context.send_activity(
            "To continue to run this bot, please fix the bot source code."
        )
        # Send a trace activity if we're talking to the Bot Framework Emulator
        if context.activity.channel_id == "emulator":
            # Create a trace activity that contains the error object
            trace_activity = Activity(
                label="TurnError",
                name="on_turn_error Trace",
                timestamp=datetime.utcnow(),
                type=ActivityTypes.trace,
                value=f"{error}",
                value_type="https://www.botframework.com/schemas/error",
            )
            # Send a trace activity, which will be displayed in Bot Framework Emulator
            await context.send_activity(trace_activity)

        if self.conversation_state:
            await self.conversation_state.delete(context)
