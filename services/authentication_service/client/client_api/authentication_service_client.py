from abc import ABC, abstractmethod
from injector import inject
from common.interface.communication_interface import CommunicationInterface
from common.interface.server_configurations_interface import ServerConfigurationsInterface
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.client.api.sign_up.sign_up_response_api import EmailSignUpResponseApi


class AuthenticationServiceClientInterface(ABC):
    @abstractmethod
    def checklivestatus(self) -> bool:
        pass

    @abstractmethod
    def email_sign_up(self, sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:
        pass

    @abstractmethod
    def email_login(self, sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:
        pass


class AuthenticationServiceClient(AuthenticationServiceClientInterface):
    @inject
    def __init__(self, server_configurations: ServerConfigurationsInterface, communication: CommunicationInterface):
        self._server_configurations = server_configurations
        self._communication = communication

    def checklivestatus(self) -> bool:
        checklivestatus_url = f'{self._server_configurations.authentication_service_config.full_server_url}/authentication_service/maintenance/checklivestatus'
        return self._communication.post()(checklivestatus_url).json()

    def email_sign_up(self, sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:
        email_sign_up_url = f'{self._server_configurations.authentication_service_config.full_server_url}/authentication_service/authentication/email_sign_up'
        response = self._communication.post()(email_sign_up_url, json=sign_up_request_api.__dict__).json()
        return EmailSignUpResponseApi(**response)

    def email_login(self, sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:
        email_login_url = f'{self._server_configurations.authentication_service_config.full_server_url}/authentication_service/authentication/email_login'
        response = self._communication.post()(email_login_url, json=sign_up_request_api.__dict__).json()
        return EmailSignUpResponseApi(**response)
