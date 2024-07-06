from abc import ABC, abstractmethod
from typing import Callable


class CommunicationInterface(ABC):
    @abstractmethod
    def get(self) -> Callable:
        pass

    @abstractmethod
    def post(self) -> Callable:
        pass

    @abstractmethod
    def patch(self) -> Callable:
        pass
