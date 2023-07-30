from injector import inject
from abc import ABC, abstractmethod
from common.interface.auto_mapper_interface import AutoMapperInterface
from services.authentication_service.core.models.sign_up.sign_up_request import EmailSignUpRequest
from services.authentication_service.core.models.sign_up.sign_up_response import EmailSignUpResponse
from services.authentication_service.core.repositories.authentication_repository import AuthenticationRepositoryInterface


class AuthenticationServiceProcessorInterface(ABC):
    @abstractmethod
    def email_sign_up(self, email_sign_up_request: EmailSignUpRequest) -> EmailSignUpResponse:
        pass


class AuthenticationServiceProcessor(AuthenticationServiceProcessorInterface):
    @inject
    def __init__(self, mapper: AutoMapperInterface, authentication_repository: AuthenticationRepositoryInterface):
        self.mapper = mapper
        self.authentication_repository = authentication_repository

    def email_sign_up(self, email_sign_up_request: EmailSignUpRequest) -> EmailSignUpResponse:
        response = self.authentication_repository.register_new_user_email(email_sign_up_request.email, email_sign_up_request.password)
        return self.mapper(response, EmailSignUpResponse)
