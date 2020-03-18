from abc import ABC
from aiohttp.web import Request, Response
from aiohttp.web_exceptions import HTTPNotImplemented

from botbuilder.core.integration import BotController


class AioHttpBotController(BotController, ABC):
    async def post(self, req: Request) -> Response:
        raise HTTPNotImplemented()

    async def get(self, req: Request) -> Response:
        raise HTTPNotImplemented()
