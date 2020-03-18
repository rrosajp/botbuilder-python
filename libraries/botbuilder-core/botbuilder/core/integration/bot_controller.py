from abc import abstractmethod, ABC

from botbuilder.core import BotAdapter, ActivityHandler


class BotController:
    def __init__(self, **kwargs):
        self.adapter = kwargs["adapter"]
        self.bot = kwargs["bot"]
