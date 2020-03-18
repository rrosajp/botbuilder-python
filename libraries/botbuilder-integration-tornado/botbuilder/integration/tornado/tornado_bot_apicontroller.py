from abc import ABC
from http import HTTPStatus

import tornado.web
import tornado.escape

from botbuilder.schema import Activity

from .tornado_bot_controller import TornadoBotController


class TornadoBotApiController(TornadoBotController, ABC):
    """
    A controller to handle incoming requests on the /api/messages path.  This is the default
    message handler for a bot.
    """

    async def post(self):
        # Main bot message handler.
        if "application/json" in self.request.headers["Content-Type"]:
            body = tornado.escape.json_decode(self.request.body)
        else:
            self.set_status(415)
            return

        activity = Activity().from_dict(body)
        auth_header = (
            self.request.headers["Authorization"] if "Authorization" in self.request.headers else ""
        )

        response = await self.adapter.process_activity(activity, auth_header, self.bot.on_turn)
        if response:
            self.write(response.body)
            self.set_status(response.status)
        else:
            self.set_status(201)

