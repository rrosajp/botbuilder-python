# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
from datetime import datetime
from types import MethodType

from aiohttp import web
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
    MemoryStorage
)
from botbuilder.schema import Activity, ActivityTypes
from activity_log import ActivityLog
from bots import MessageReactionBot
# from threading_helper import run_coroutine
from config import DefaultConfig

# Create the Flask app
CONFIG = DefaultConfig()
PORT = CONFIG.PORT

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)


# Catch-all for errors.
async def on_error( # pylint: disable=unused-argument
    self, context: TurnContext, error: Exception
):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)

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


ADAPTER.on_turn_error = MethodType(on_error, ADAPTER)

MEMORY = MemoryStorage()
ACTIVITY_LOG = ActivityLog(MEMORY)
# Create the Bot
BOT = MessageReactionBot(ACTIVITY_LOG)

# Listen for incoming requests on /api/messages.s
async def messages(req: web.Request) -> web.Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return web.Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = (
        req.headers["Authorization"] if "Authorization" in req.headers else ""
    )

    try:
        await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        return web.Response(status=201)
    except Exception as exception:
        raise exception


APP = web.Application()
APP.router.add_post("/api/messages", messages)

try:
    web.run_app(APP, host="localhost", port=PORT)
except Exception as error:
    raise error
