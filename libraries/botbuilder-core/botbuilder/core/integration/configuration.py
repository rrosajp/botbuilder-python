from abc import abstractmethod, ABC


class Configuration(ABC):
    @abstractmethod
    def get(self, key: str) -> str:
        raise NotImplementedError()

    def all(self) -> dict:
        raise NotImplementedError()

    def __getitem__(self, item):
        return self.get(item)
