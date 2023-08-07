from abc import ABC, abstractmethod
from common.objects.service_config import ServiceConfig


class ServerConfigurationsInterface(ABC):
    @property
    @abstractmethod
    def frontend_server_config(self) -> ServiceConfig:
        pass

    @property
    @abstractmethod
    def authentication_service_config(self) -> ServiceConfig:
        pass
