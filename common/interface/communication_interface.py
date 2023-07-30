from abc import ABC, abstractmethod
from typing import Callable


class CommunicationInterface(ABC):
    @abstractmethod
    def post(self) -> Callable:
        pass
