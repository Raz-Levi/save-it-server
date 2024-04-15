from abc import ABC, abstractmethod
from typing import Any


class InjectorInterface(ABC):
    @abstractmethod
    def inject(self, class_type: Any) -> None:
        pass
