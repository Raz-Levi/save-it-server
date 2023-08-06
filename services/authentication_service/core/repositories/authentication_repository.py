from injector import inject
from abc import ABC, abstractmethod
from common.interface.communication_interface import CommunicationInterface
from services.authentication_service.core.configurations.authentication_service_config import AuthenticationConfigurationsInterface
from services.authentication_service.core.models.dal.dal_authentication_response import DalAuthenticationResponse
from services.authentication_service.common.enums.email_sign_up_status import EmailSignUpStatus


class AuthenticationRepositoryInterface(ABC):
    @abstractmethod
    def register_new_user_email(self, email: str, password: str) -> DalAuthenticationResponse:
        pass

    @abstractmethod
    def login_email(self, email: str, password: str) -> DalAuthenticationResponse:
        pass


class AuthenticationRepository(AuthenticationRepositoryInterface):
    @inject
    def __init__(self, communication: CommunicationInterface, configurations: AuthenticationConfigurationsInterface):
        self._communication = communication
        self._configurations = configurations

    def register_new_user_email(self, email: str, password: str) -> DalAuthenticationResponse:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = self._communication.post()(self._configurations.signup_url, json=payload).json()

        if 'idToken' in response:
            return DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=response['idToken'])

        elif 'error' in response:
            match response['error']['message']:
                case "EMAIL_EXISTS":
                    return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.EMAIL_EXISTS)

                case "INVALID_EMAIL":
                    return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.INVALID_EMAIL)

        return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.UNKNOWN_ERROR)

    def login_email(self, email: str, password: str) -> DalAuthenticationResponse:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = self._communication.post()(self._configurations.login_url, json=payload).json()

        if 'idToken' in response:
            return DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=response['idToken'])

        elif 'error' in response:
            match response['error']['message']:
                case "EMAIL_NOT_FOUND":
                    return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.EMAIL_NOT_FOUND)

                case "INVALID_PASSWORD":
                    return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.INVALID_PASSWORD)

        return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.UNKNOWN_ERROR)
