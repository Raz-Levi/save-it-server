from injector import inject
import json
from abc import ABC, abstractmethod
from common.interface.communication_interface import CommunicationInterface
from common.objects.logger import LoggerInterface
from services.user_information_service.core.configurations.user_information_service_config import UserInformationConfigurationsInterface
from services.user_information_service.core.models.dal.user_information.dal_get_user_information_response import DalGetUserInformationResponse
from services.user_information_service.core.models.dal.user_information.dal_set_user_information_response import DalSetUserInformationDalResponse
from services.user_information_service.core.models.dal.user_information.dal_user_information import DalUserInformation


class UserInformationRepositoryInterface(ABC):
    @abstractmethod
    def set_user_information_by_user_id(self, user_id: str, user_information: DalUserInformation) -> DalSetUserInformationDalResponse:
        pass

    @abstractmethod
    def get_user_information_by_user_id(self, user_id: str) -> DalGetUserInformationResponse:
        pass


class UserInformationRepository(UserInformationRepositoryInterface):
    @inject
    def __init__(self, communication: CommunicationInterface, configurations: UserInformationConfigurationsInterface, logger: LoggerInterface):
        self._communication = communication
        self._configurations = configurations
        self._logger = logger
        self._database_collection_id = "user_information"

    def set_user_information_by_user_id(self, user_id: str, user_information: DalUserInformation) -> DalSetUserInformationDalResponse:
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "fields": {
                "email": {"stringValue": user_information.email},
                "full_name": {"stringValue": user_information.full_name},
                "phone": {"stringValue": user_information.phone},
                "user_id": {"stringValue": user_information.user_id},
            }
        }

        try:
            response = self._communication.patch()(self._configurations.user_information_database_url(self._database_collection_id, user_id), headers=headers, data=json.dumps(data))

        except Exception as e:
            self._logger.critical(f"Setting User Information Failed: {e}")
            return DalSetUserInformationDalResponse(is_success=False)

        if response.ok:
            self._logger.info(f'Setting User Information Success if user id {user_id}')
            return DalSetUserInformationDalResponse(is_success=True)

        return DalSetUserInformationDalResponse(is_success=False)

    def get_user_information_by_user_id(self, user_id: str) -> DalGetUserInformationResponse:
        try:
            response = self._communication.get()(self._configurations.user_information_database_url(self._database_collection_id, user_id))

        except Exception as e:
            self._logger.critical(f"Getting User Information Failure: {e}")
            return DalGetUserInformationResponse(is_success=False, dal_user_information=None)

        if response.ok:
            try:
                response_json = response.json()
                dal_user_information = DalUserInformation(
                    email=response_json['fields']['email']['stringValue'],
                    full_name=response_json['fields']['full_name']['stringValue'],
                    phone=response_json['fields']['phone']['stringValue'],
                    user_id=response_json['fields']['user_id']['stringValue']
                )

            except Exception as e:
                self._logger.critical(f"Getting User Information Failure in parse phase: {e}")
                return DalGetUserInformationResponse(is_success=False, dal_user_information=None)

            self._logger.info(f'Getting User Information Success if user id {user_id}')
            return DalGetUserInformationResponse(is_success=True, dal_user_information=dal_user_information)

        return DalGetUserInformationResponse(is_success=False, dal_user_information=None)
