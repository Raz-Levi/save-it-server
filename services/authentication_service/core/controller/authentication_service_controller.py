from injector import inject
from abc import ABC, abstractmethod
from common.interface.auto_mapper_interface import AutoMapperInterface
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.client.api.sign_up.sign_up_response_api import EmailSignUpResponseApi
from services.authentication_service.core.processor.authentication_service_processor import AuthenticationServiceProcessorInterface
from services.authentication_service.core.models.sign_up.sign_up_request import EmailSignUpRequest


class AuthenticationServiceControllerInterface(ABC):
    @abstractmethod
    def email_sign_up(self, email_sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:
        pass


class AuthenticationServiceController(AuthenticationServiceControllerInterface):
    @inject
    def __init__(self, mapper: AutoMapperInterface, authentication_service_processor: AuthenticationServiceProcessorInterface):
        self.mapper = mapper
        self.authentication_service_processor = authentication_service_processor

    def email_sign_up(self, email_sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:
        email_sign_up_request = self.mapper(email_sign_up_request_api, EmailSignUpRequest)
        email_sign_up_result = self.authentication_service_processor.email_sign_up(email_sign_up_request)
        return self.mapper(email_sign_up_result, EmailSignUpResponseApi)
