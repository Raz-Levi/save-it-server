from abc import ABC, abstractmethod
from injector import inject
from common.interface.communication_interface import CommunicationInterface
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.client.api.sign_up.sign_up_response_api import EmailSignUpResponseApi
from services.authentication_service.client.api.checklivestatus.authentication_check_live_status_response_api import AuthenticationCheckLiveStatusResponseApi
from services.authentication_service.configuration.authentication_service_configuration_base import AuthenticationServiceConfigurationBase


class AuthenticationServiceClientInterface(ABC):
    @abstractmethod
    def checklivestatus(self) -> AuthenticationCheckLiveStatusResponseApi:
        pass

    @abstractmethod
    def email_sign_up(self, sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:
        pass

    @abstractmethod
    def email_login(self, sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:
        pass


class AuthenticationServiceClient(AuthenticationServiceClientInterface):
    @inject
    def __init__(self, authentication_service_configurations: AuthenticationServiceConfigurationBase, communication: CommunicationInterface):
        self._authentication_service_configurations = authentication_service_configurations
        self._communication = communication

    def checklivestatus(self) -> AuthenticationCheckLiveStatusResponseApi:
        checklivestatus_url = f'{self._authentication_service_configurations.full_server_url}/authentication_service/maintenance/checklivestatus'
        response = self._communication.post()(checklivestatus_url).json()
        return AuthenticationCheckLiveStatusResponseApi(**response)

    def email_sign_up(self, sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:
        email_sign_up_url = f'{self._authentication_service_configurations.full_server_url}/authentication_service/authentication/email_sign_up'
        response = self._communication.post()(email_sign_up_url, json=sign_up_request_api.__dict__).json()
        return EmailSignUpResponseApi(**response)

    def email_login(self, sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:
        email_login_url = f'{self._authentication_service_configurations.full_server_url}/authentication_service/authentication/email_login'
        response = self._communication.post()(email_login_url, json=sign_up_request_api.__dict__).json()
        return EmailSignUpResponseApi(**response)
