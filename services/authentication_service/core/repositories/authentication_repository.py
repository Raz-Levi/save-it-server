from injector import inject
from abc import ABC, abstractmethod
from common.interface.communication_interface import CommunicationInterface
from services.authentication_service.core.configurations.authentication_service_config import AuthenticationConfigurationsInterface
from services.authentication_service.core.models.dal.dal_authentication_response import DalAuthenticationResponse
from services.authentication_service.client.enums.email_sign_up_status import EmailSignUpStatus


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
        self.communication = communication
        self.configurations = configurations

    def register_new_user_email(self, email: str, password: str) -> DalAuthenticationResponse:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = self.communication.post()(self.configurations.get_signup_url(), json=payload).json()

        if 'idToken' in response:
            return DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=response['idToken'])

        elif 'error' in response and response['error']['message'] == "EMAIL_EXISTS":
            return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.EMAIL_EXISTS)

        else:
            return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.UNKNOWN_ERROR)

    def login_email(self, email: str, password: str) -> DalAuthenticationResponse:
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = self.communication.post()(self.configurations.get_signin_password_url(), json=payload).json()

        if 'idToken' in response:
            return DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=response['idToken'])

        elif 'error' in response and response['error']['message'] == "EMAIL_NOT_FOUND":
            return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.EMAIL_NOT_FOUND)

        else:
            return DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.UNKNOWN_ERROR)
