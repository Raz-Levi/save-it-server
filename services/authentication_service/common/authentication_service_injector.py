from injector import Injector, Module, Binder
from typing import Any
from services.authentication_service.core.controller.authentication_service_controller import AuthenticationServiceController
from common.interface.auto_mapper_interface import AutoMapperInterface
from services.authentication_service.common.authentication_service_auto_mapper import AuthenticationServiceAutoMapper
from services.authentication_service.core.processor.authentication_service_processor import AuthenticationServiceProcessorInterface, AuthenticationServiceProcessor
from services.authentication_service.core.repositories.authentication_repository import AuthenticationRepositoryInterface, AuthenticationRepository
from services.authentication_service.core.configurations.authentication_service_config import AuthenticationConfigurationsInterface, AuthenticationConfigurations
from common.interface.communication_interface import CommunicationInterface
from common.objects.communication import Communication


class AuthenticationServiceInjector:
    @staticmethod
    def inject(class_type: Any) -> None:
        class _AuthenticationServiceInjector(Module):
            def configure(self, binder: Binder):
                binder.bind(AutoMapperInterface, to=AuthenticationServiceAutoMapper)
                binder.bind(AuthenticationServiceProcessorInterface, to=AuthenticationServiceProcessor)
                binder.bind(AuthenticationRepositoryInterface, to=AuthenticationRepository)
                binder.bind(AuthenticationConfigurationsInterface, to=AuthenticationConfigurations)
                binder.bind(CommunicationInterface, to=Communication)

        return Injector(modules=[_AuthenticationServiceInjector()]).get(class_type)


if __name__ == '__main__':
    controller = AuthenticationServiceInjector.inject(AuthenticationServiceController)

    from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
    response = controller.email_sign_up(EmailSignUpRequestApi("raz@qa.qa", "qaqaqa"))
    print(response)