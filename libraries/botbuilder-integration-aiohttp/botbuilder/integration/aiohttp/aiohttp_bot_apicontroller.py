from abc import ABC
from http import HTTPStatus

from aiohttp.web import Request, Response, json_response
from botbuilder.schema import Activity

from .aiohttp_bot_controller import AioHttpBotController


class AioHttpBotApiController(AioHttpBotController, ABC):
    """
    A controller to handle incoming requests on the /api/messages path.  This is the default
    message handler for a bot.
    """

    async def post(self, req: Request) -> Response:
        """
        Main bot message handler.
        """

        if "application/json" in req.headers["Content-Type"]:
            body = await req.json()
        else:
            return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        activity = Activity().deserialize(body)
        auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

        response = await self.adapter.process_activity(activity, auth_header, self.bot.on_turn)
        if response:
            return json_response(data=response.body, status=response.status)
        return Response(status=HTTPStatus.CREATED)
