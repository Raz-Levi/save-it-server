from injector import Injector, Module, Binder
from typing import Any
from common.interface.server_configurations_interface import ServerConfigurationsInterface
from common.configuration.server_configutrations.server_configurations_local import ServerConfigurationsLocal
from common.interface.auto_mapper_interface import AutoMapperInterface
from common.interface.communication_interface import CommunicationInterface
from common.objects.communication import Communication
from services.frontend_server.common.frontend_server_auto_mapper import FrontendServerAutoMapper
from services.frontend_server.core.controller.frontend_server_controller import FrontendServerControllerInterface, FrontendServerController
from services.authentication_service.client.client_api.authentication_service_client import AuthenticationServiceClientInterface, AuthenticationServiceClient
from services.frontend_server.core.processor.frontend_server_processor import FrontendServerProcessorInterface, FrontendServerProcessor


class FrontendServerInjector:
    @staticmethod
    def inject(class_type: Any) -> None:
        class _FrontendServerInjector(Module):
            def configure(self, binder: Binder):
                binder.bind(FrontendServerControllerInterface, to=FrontendServerController)
                binder.bind(FrontendServerProcessorInterface, to=FrontendServerProcessor)
                binder.bind(AutoMapperInterface, to=FrontendServerAutoMapper)
                binder.bind(AuthenticationServiceClientInterface, to=AuthenticationServiceClient)
                binder.bind(CommunicationInterface, to=Communication)
                binder.bind(ServerConfigurationsInterface, to=ServerConfigurationsLocal)  # TODO- update tp QA and Prod

        return Injector(modules=[_FrontendServerInjector()]).get(class_type)
