from injector import Injector, Module, Binder
from typing import Any
from common.enums.environment_configuration import EnvironmentConfiguration
from common.interface.InjectorInterface import InjectorInterface
from common.interface.auto_mapper_interface import AutoMapperInterface
from common.interface.communication_interface import CommunicationInterface
from common.objects.communication import Communication
from services.authentication_service.configuration.authentication_service_configuration_base import AuthenticationServiceConfigurationBase
from services.authentication_service.configuration.authentication_service_configuration_factory import AuthenticationServiceConfigurationFactory
from services.frontend_server.common.frontend_server_auto_mapper import FrontendServerAutoMapper
from services.frontend_server.core.controller.frontend_server_controller import FrontendServerControllerInterface, FrontendServerController
from services.authentication_service.client.client_api.authentication_service_client import AuthenticationServiceClientInterface, AuthenticationServiceClient
from services.frontend_server.core.processor.frontend_server_processor import FrontendServerProcessorInterface, FrontendServerProcessor


class FrontendServerInjector(InjectorInterface):
    def __init__(self, environment_configuration: EnvironmentConfiguration = EnvironmentConfiguration.LOCAL):
        self.environment_configuration = environment_configuration

    def inject(self, class_type: Any) -> None:
        environment_configuration = self.environment_configuration

        class _FrontendServerInjector(Module):
            def configure(self, binder: Binder) -> None:
                binder.bind(FrontendServerControllerInterface, to=FrontendServerController)
                binder.bind(FrontendServerProcessorInterface, to=FrontendServerProcessor)
                binder.bind(AutoMapperInterface, to=FrontendServerAutoMapper)
                binder.bind(AuthenticationServiceClientInterface, to=AuthenticationServiceClient)
                binder.bind(CommunicationInterface, to=Communication)
                binder.bind(AuthenticationServiceConfigurationBase, to=AuthenticationServiceConfigurationFactory()(environment_configuration))

        return Injector(modules=[_FrontendServerInjector()]).get(class_type)
