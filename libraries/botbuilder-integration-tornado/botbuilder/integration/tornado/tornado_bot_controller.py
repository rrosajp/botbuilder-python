from abc import ABC
import tornado.web
from botbuilder.core import ActivityHandler, BotAdapter

from botbuilder.core.integration import BotController
from tornado import httputil
from tornado.httpclient import HTTPError


class TornadoBotController(BotController, tornado.web.RequestHandler, ABC):
    def __init__(
        self, application: "Application", request: httputil.HTTPServerRequest, **kwargs
    ):
        # This needs to be reviewed.  In the Tornado samples, a message handler derives
        # from RequestHandler, and has an initialize method that takes an adapter and
        # a bot (with no __init__).  That doesn't seem to work here so each __init__
        # is being called, and there is no initialize method.
        BotController.__init__(self, **kwargs)
        tornado.web.RequestHandler.__init__(self, application, request, **{})

    async def post(self):
        raise HTTPError(405)

    async def get(self):
        raise HTTPError(405)
