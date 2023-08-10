from injector import inject
from abc import ABC, abstractmethod
from common.interface.communication_interface import CommunicationInterface
from services.authentication_service.core.configurations.authentication_service_config import AuthenticationConfigurationsInterface
from services.authentication_service.core.models.dal.dal_authentication_response import DalAuthenticationResponse
from services.authentication_service.common.enums.email_sign_up_status import EmailSignUpStatus
from common.objects.logger import LoggerInterface


class AuthenticationRepositoryInterface(ABC):
    @abstractmethod
    def register_new_user_email(self, email: str, password: str) -> DalAuthenticationResponse:
        pass

    @abstractmethod
    def login_email(self, email: str, password: str) -> DalAuthenticationResponse:
        pass


class AuthenticationRepository(AuthenticationRepositoryInterface):
    @inject
    def __init__(self, communication: CommunicationInterface, configurations: AuthenticationConfigurationsInterface, logger: LoggerInterface):
        self._communication = communication
        self._configurations = configurations
        self._logger = logger

    def register_new_user_email(self, email: str, password: str) -> DalAuthenticationResponse:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = self._communication.post()(self._configurations.signup_url, json=payload).json()

        if 'idToken' in response:
            self._logger.log_info("Email SignUp Success")
            return DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=response['idToken'])

        elif 'error' in response:
            match response['error']['message']:
                case "EMAIL_EXISTS":
                    self._logger.log_info("Email SignUp Failure")
                    return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.EMAIL_EXISTS)

                case "INVALID_EMAIL":
                    self._logger.log_info("Email SignUp Failure")
                    return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.INVALID_EMAIL)

        self._logger.log_critical("Email SignUp Failure for Unknown Reason")
        return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.UNKNOWN_ERROR)

    def login_email(self, email: str, password: str) -> DalAuthenticationResponse:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = self._communication.post()(self._configurations.login_url, json=payload).json()

        if 'idToken' in response:
            self._logger.log_info("Email Login Success")
            return DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=response['idToken'])

        elif 'error' in response:
            match response['error']['message']:
                case "EMAIL_NOT_FOUND":
                    self._logger.log_info("Email Login Failure")
                    return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.EMAIL_NOT_FOUND)

                case "INVALID_PASSWORD":
                    self._logger.log_info("Email Login Failure")
                    return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.INVALID_PASSWORD)

        self._logger.log_critical("Email Login Failure for Unknown Reason")
        return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.UNKNOWN_ERROR)
