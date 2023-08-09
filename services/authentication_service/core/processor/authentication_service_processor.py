from injector import inject
from abc import ABC, abstractmethod
from common.interface.auto_mapper_interface import AutoMapperInterface
from services.authentication_service.core.models.sign_up.sign_up_request import EmailSignUpRequest
from services.authentication_service.core.models.sign_up.sign_up_response import EmailSignUpResponse
from services.authentication_service.core.repositories.authentication_repository import AuthenticationRepositoryInterface
from services.authentication_service.core.models.checklivestatus.authentication_check_live_status_response import AuthenticationCheckLiveStatusResponse
from common.enums.server_live_status import ServerLiveStatus

class AuthenticationServiceProcessorInterface(ABC):
    @abstractmethod
    def checklivestatus(self) -> AuthenticationCheckLiveStatusResponse:
        pass

    @abstractmethod
    def email_sign_up(self, email_sign_up_request: EmailSignUpRequest) -> EmailSignUpResponse:
        pass

    @abstractmethod
    def email_login(self, email_sign_up_request: EmailSignUpRequest) -> EmailSignUpResponse:
        pass


class AuthenticationServiceProcessor(AuthenticationServiceProcessorInterface):
    @inject
    def __init__(self, mapper: AutoMapperInterface, authentication_repository: AuthenticationRepositoryInterface):
        self._mapper = mapper
        self._authentication_repository = authentication_repository

    def checklivestatus(self) -> AuthenticationCheckLiveStatusResponse:
        return AuthenticationCheckLiveStatusResponse(ServerLiveStatus.ALIVE)

    def email_sign_up(self, email_sign_up_request: EmailSignUpRequest) -> EmailSignUpResponse:
        response = self._authentication_repository.register_new_user_email(email_sign_up_request.email, email_sign_up_request.password)
        return self._mapper(response, EmailSignUpResponse)

    def email_login(self, email_sign_up_request: EmailSignUpRequest) -> EmailSignUpResponse:
        response = self._authentication_repository.login_email(email_sign_up_request.email, email_sign_up_request.password)
        return self._mapper(response, EmailSignUpResponse)
