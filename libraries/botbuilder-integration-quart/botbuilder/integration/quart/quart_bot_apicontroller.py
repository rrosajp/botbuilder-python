from http import HTTPStatus
from quart import Response, request
from botbuilder.schema import Activity

from .quart_bot_controller import QuartBotController


class QuartBotApiController(QuartBotController):
    """
    A controller to handle incoming requests on the /api/messages path.  This is the default
    message handler for a bot.
    """

    async def messages(self) -> Response:
        """
        Main bot message handler.
        """

        if "application/json" in request.headers["Content-Type"]:
            body = await request.json
        else:
            return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        activity = Activity().deserialize(body)
        auth_header = (
            request.headers["Authorization"]
            if "Authorization" in request.headers
            else ""
        )

        response = await self.adapter.process_activity(
            activity, auth_header, self.bot.on_turn
        )
        if response:
            # TODO return InvokeResponse.body
            return Response("", status=HTTPStatus.CREATED)
        return Response("", status=HTTPStatus.CREATED)
