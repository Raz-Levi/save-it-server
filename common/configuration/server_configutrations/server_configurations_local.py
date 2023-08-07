from common.interface.server_configurations_interface import ServerConfigurationsInterface
from common.objects.service_config import ServiceConfig


class ServerConfigurationsLocal(ServerConfigurationsInterface):
    @property
    def frontend_server_config(self) -> ServiceConfig:
        return ServiceConfig("http://127.0.0.1", 40000)

    @property
    def authentication_service_config(self) -> ServiceConfig:
        return ServiceConfig("http://127.0.0.1", 8080)
