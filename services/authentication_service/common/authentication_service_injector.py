from injector import Injector, Module, Binder
from typing import Any
from common.enums.environment_configuration import EnvironmentConfiguration
from common.interface.InjectorInterface import InjectorInterface
from common.interface.auto_mapper_interface import AutoMapperInterface
from services.authentication_service.common.authentication_service_auto_mapper import AuthenticationServiceAutoMapper
from services.authentication_service.core.controller.authentication_service_controller import AuthenticationServiceControllerInterface, AuthenticationServiceController
from services.authentication_service.core.processor.authentication_service_processor import AuthenticationServiceProcessorInterface, AuthenticationServiceProcessor
from services.authentication_service.core.repositories.authentication_repository import AuthenticationRepositoryInterface, AuthenticationRepository
from services.authentication_service.core.configurations.authentication_service_config import AuthenticationConfigurationsInterface, AuthenticationConfigurations
from common.interface.communication_interface import CommunicationInterface
from common.objects.communication import Communication
from services.authentication_service.core.configurations.authentication_preferences import AuthenticationPreferencesInterface, AuthenticationPreferences
from common.objects.logger import Logger, LoggerInterface


class AuthenticationServiceInjector(InjectorInterface):
    def __init__(self, environment_configuration: EnvironmentConfiguration = EnvironmentConfiguration.LOCAL):
        self.environment_configuration = environment_configuration

    def inject(self, class_type: Any) -> None:
        class _AuthenticationServiceInjector(Module):
            def configure(self, binder: Binder) -> None:
                binder.bind(AuthenticationServiceControllerInterface, to=AuthenticationServiceController)
                binder.bind(AutoMapperInterface, to=AuthenticationServiceAutoMapper)
                binder.bind(AuthenticationServiceProcessorInterface, to=AuthenticationServiceProcessor)
                binder.bind(AuthenticationRepositoryInterface, to=AuthenticationRepository)
                binder.bind(AuthenticationConfigurationsInterface, to=AuthenticationConfigurations)
                binder.bind(CommunicationInterface, to=Communication)
                binder.bind(AuthenticationPreferencesInterface, to=AuthenticationPreferences)
                binder.bind(LoggerInterface, to=Logger)

        return Injector(modules=[_AuthenticationServiceInjector()]).get(class_type)
