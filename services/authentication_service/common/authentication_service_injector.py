from injector import Injector, Module, Binder
from typing import Any
from services.authentication_service.core.controller.authentication_service_controller import AuthenticationServiceController
from services.authentication_service.common.authentication_service_auto_mapper import AuthenticationServiceAutoMapper
from services.authentication_service.core.processor.authentication_service_processor import AuthenticationServiceProcessor
from services.authentication_service.core.repositories.authentication_repository import AuthenticationRepository
from services.authentication_service.core.configurations.authentication_service_config import AuthenticationConfigurations
from common.interface.communication_interface import CommunicationInterface
from common.objects.communication import Communication


class AuthenticationServiceInjector:
    @staticmethod
    def inject(class_type: Any) -> Any:  # TODO- create interfaces
        class _AuthenticationServiceInjector(Module):
            def configure(self, binder: Binder):
                binder.bind(AuthenticationServiceAutoMapper)
                binder.bind(AuthenticationServiceProcessor)
                binder.bind(AuthenticationRepository)
                binder.bind(AuthenticationConfigurations)
                binder.bind(CommunicationInterface, to=Communication)

        return Injector(modules=[_AuthenticationServiceInjector()]).get(class_type)


if __name__ == '__main__':
    controller = AuthenticationServiceInjector.inject(AuthenticationServiceController)

    from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
    controller.email_sign_up(EmailSignUpRequestApi("raz@qa.qa", "qaqaqa"))
