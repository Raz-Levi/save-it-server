from abc import ABC, abstractmethod
from injector import inject
from common.interface.communication_interface import CommunicationInterface
from services.user_information_service.client.api.checklivestatus.user_information_check_live_status_response_api import UserInformationCheckLiveStatusResponseApi
from services.user_information_service.client.api.get_user_information.get_user_information_request_api import GetUserInformationRequestApi
from services.user_information_service.client.api.get_user_information.get_user_information_response_api import GetUserInformationResponseApi
from services.user_information_service.client.api.set_user_information.set_user_information_request_api import SetUserInformationRequestApi
from services.user_information_service.client.api.set_user_information.set_user_information_response_api import SetUserInformationResponseApi
from services.user_information_service.configuration.user_information_service_configuration_base import UserInformationServiceConfigurationBase


class UserInformationServiceClientInterface(ABC):
    @abstractmethod
    def checklivestatus(self) -> UserInformationCheckLiveStatusResponseApi:
        pass

    @abstractmethod
    def set_user_information(self, set_user_information_request_api: SetUserInformationRequestApi) -> SetUserInformationResponseApi:
        pass

    @abstractmethod
    def get_user_information(self, set_user_information_request_api: GetUserInformationRequestApi) -> GetUserInformationResponseApi:
        pass


class UserInformationServiceClient(UserInformationServiceClientInterface):
    @inject
    def __init__(self, user_information_service_configurations: UserInformationServiceConfigurationBase, communication: CommunicationInterface):
        self._user_information_service_configurations = user_information_service_configurations
        self._communication = communication

    def checklivestatus(self) -> UserInformationCheckLiveStatusResponseApi:
        checklivestatus_url = f'{self._user_information_service_configurations.full_server_url}/user_information_service/maintenance/checklivestatus'
        response = self._communication.post()(checklivestatus_url).json()
        return UserInformationCheckLiveStatusResponseApi(**response)

    def set_user_information(self, set_user_information_request_api: SetUserInformationRequestApi) -> SetUserInformationResponseApi:
        email_sign_up_url = f'{self._user_information_service_configurations.full_server_url}/user_information_service/set_user_information'
        response = self._communication.post()(email_sign_up_url, json=set_user_information_request_api.__dict__).json()
        return SetUserInformationResponseApi(**response)

    def get_user_information(self, get_user_information_request_api: GetUserInformationRequestApi) -> GetUserInformationResponseApi:
        email_sign_up_url = f'{self._user_information_service_configurations.full_server_url}/user_information_service/get_user_information'
        response = self._communication.post()(email_sign_up_url, json=get_user_information_request_api.__dict__).json()
        return GetUserInformationResponseApi(**response)
