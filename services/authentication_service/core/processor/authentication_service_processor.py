from injector import inject
from abc import ABC, abstractmethod
import re
from common.interface.auto_mapper_interface import AutoMapperInterface
from services.authentication_service.core.models.sign_up.sign_up_request import EmailSignUpRequest
from services.authentication_service.core.models.sign_up.sign_up_response import EmailSignUpResponse
from services.authentication_service.core.repositories.authentication_repository import AuthenticationRepositoryInterface
from services.authentication_service.core.models.checklivestatus.authentication_check_live_status_response import AuthenticationCheckLiveStatusResponse
from common.enums.server_live_status import ServerLiveStatus
from services.authentication_service.common.enums.email_sign_up_status import EmailSignUpStatus
from services.authentication_service.core.configurations.authentication_preferences import AuthenticationPreferencesInterface


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
    def __init__(self, mapper: AutoMapperInterface, authentication_repository: AuthenticationRepositoryInterface, authentication_preferences: AuthenticationPreferencesInterface):
        self._mapper = mapper
        self._authentication_repository = authentication_repository
        self._authentication_preferences = authentication_preferences

    def checklivestatus(self) -> AuthenticationCheckLiveStatusResponse:
        return AuthenticationCheckLiveStatusResponse(ServerLiveStatus.ALIVE)

    def email_sign_up(self, email_sign_up_request: EmailSignUpRequest) -> EmailSignUpResponse:
        if not self._is_valid_email(email_sign_up_request.email):
            return EmailSignUpResponse(is_success=False, status=EmailSignUpStatus.INVALID_EMAIL)

        if not self._is_valid_password(email_sign_up_request.password):
            return EmailSignUpResponse(is_success=False, status=EmailSignUpStatus.INVALID_PASSWORD)

        response = self._authentication_repository.register_new_user_email(email_sign_up_request.email, email_sign_up_request.password)
        return self._mapper(response, EmailSignUpResponse)

    def email_login(self, email_sign_up_request: EmailSignUpRequest) -> EmailSignUpResponse:
        if not self._is_valid_email(email_sign_up_request.email):
            return EmailSignUpResponse(is_success=False, status=EmailSignUpStatus.INVALID_EMAIL)

        response = self._authentication_repository.login_email(email_sign_up_request.email, email_sign_up_request.password)
        return self._mapper(response, EmailSignUpResponse)

    ############### Private ###############
    def _is_valid_email(self, email):
        valid_email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(valid_email_pattern, email)

    def _is_valid_password(self, password) -> bool:
        has_lowercase = not self._authentication_preferences.password_must_lowercase or re.search(r'[a-z]', password)
        has_uppercase = not self._authentication_preferences.password_must_uppercase or re.search(r'[A-Z]', password)
        has_digit = not self._authentication_preferences.password_must_digit or re.search(r'\d', password)
        has_special_char = not self._authentication_preferences.password_must_special_char or re.search(r'[!@#$%^&*()-_=+{}\[\]:;,.<>?/\\|]', password)
        return len(password) >= self._authentication_preferences.min_password_length and has_lowercase and has_uppercase and has_digit and has_special_char
