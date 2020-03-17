import os
from configparser import ConfigParser

from .configuration import Configuration


class DefaultConfiguration(Configuration):
    def __init__(self, path: str = "appsettings.properties"):
        self.config = ConfigParser()
        self.config.read(path)

    def get(self, key: str) -> str:
        value = self.config.get("bot", key)
        if not value:
            value = os.environ.get(key)
        return value
