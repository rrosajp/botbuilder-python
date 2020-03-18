from quart import Response
from botbuilder.core.integration import BotController


class QuartBotController(BotController):
    async def messages(self):
        return Response("", status=405)
