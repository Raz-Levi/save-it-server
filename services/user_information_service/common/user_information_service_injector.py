from injector import Injector, Module, Binder
from typing import Any
from common.enums.environment_configuration import EnvironmentConfiguration
from common.interface.InjectorInterface import InjectorInterface
from common.interface.auto_mapper_interface import AutoMapperInterface
from common.interface.communication_interface import CommunicationInterface
from common.objects.communication import Communication
from common.objects.logger import Logger, LoggerInterface
from services.user_information_service.common.user_information_service_auto_mapper import UserInformationServiceAutoMapper
from services.user_information_service.core.configurations.user_information_service_config import UserInformationConfigurationsInterface, UserInformationConfigurations
from services.user_information_service.core.controller.user_information_service_controller import UserInformationServiceControllerInterface, UserInformationServiceController
from services.user_information_service.core.processor.user_information_service_processor import UserInformationServiceProcessorInterface, UserInformationServiceProcessor
from services.user_information_service.core.repositories.user_information_repository import UserInformationRepository, UserInformationRepositoryInterface


class UserInformationServiceInjector(InjectorInterface):
    def __init__(self, environment_configuration: EnvironmentConfiguration = EnvironmentConfiguration.LOCAL):
        self.environment_configuration = environment_configuration

    def inject(self, class_type: Any) -> None:
        class _UserInformationServiceInjector(Module):
            def configure(self, binder: Binder) -> None:
                binder.bind(UserInformationServiceControllerInterface, to=UserInformationServiceController)
                binder.bind(AutoMapperInterface, to=UserInformationServiceAutoMapper)
                binder.bind(UserInformationServiceProcessorInterface, to=UserInformationServiceProcessor)
                binder.bind(UserInformationRepositoryInterface, to=UserInformationRepository)
                binder.bind(UserInformationConfigurationsInterface, to=UserInformationConfigurations)
                binder.bind(CommunicationInterface, to=Communication)
                binder.bind(LoggerInterface, to=Logger)

        return Injector(modules=[_UserInformationServiceInjector()]).get(class_type)
