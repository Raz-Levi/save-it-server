from injector import inject
from abc import ABC, abstractmethod
from common.interface.auto_mapper_interface import AutoMapperInterface
from services.user_information_service.client.api.checklivestatus.user_information_check_live_status_response_api import UserInformationCheckLiveStatusResponseApi
from services.user_information_service.client.api.get_user_information.get_user_information_request_api import GetUserInformationRequestApi
from services.user_information_service.client.api.get_user_information.get_user_information_response_api import GetUserInformationResponseApi
from services.user_information_service.client.api.set_user_information.set_user_information_request_api import SetUserInformationRequestApi
from services.user_information_service.client.api.set_user_information.set_user_information_response_api import SetUserInformationResponseApi
from services.user_information_service.core.models.get_user_information.get_user_information_request import GetUserInformationRequest
from services.user_information_service.core.models.set_user_information.set_user_information_request import SetUserInformationRequest
from services.user_information_service.core.processor.user_information_service_processor import UserInformationServiceProcessorInterface


class UserInformationServiceControllerInterface(ABC):
    @abstractmethod
    def checklivestatus(self) -> UserInformationCheckLiveStatusResponseApi:
        pass

    @abstractmethod
    def set_user_information(self, set_user_information_request_api: SetUserInformationRequestApi) -> SetUserInformationResponseApi:
        pass

    @abstractmethod
    def get_user_information(self, set_user_information_request_api: GetUserInformationRequestApi) -> GetUserInformationResponseApi:
        pass


class UserInformationServiceController(UserInformationServiceControllerInterface):
    @inject
    def __init__(self, mapper: AutoMapperInterface, user_information_service_processor: UserInformationServiceProcessorInterface):
        self._mapper = mapper
        self._user_information_service_processor = user_information_service_processor

    def checklivestatus(self) -> UserInformationCheckLiveStatusResponseApi:
        checklivestatus_result = self._user_information_service_processor.checklivestatus()
        return self._mapper(checklivestatus_result, UserInformationCheckLiveStatusResponseApi)

    def set_user_information(self, set_user_information_request_api: SetUserInformationRequestApi) -> SetUserInformationResponseApi:
        set_user_information_request = self._mapper(set_user_information_request_api, SetUserInformationRequest)
        set_user_information_result = self._user_information_service_processor.set_user_information(set_user_information_request)
        return self._mapper(set_user_information_result, SetUserInformationResponseApi)

    def get_user_information(self, get_user_information_request_api: GetUserInformationRequestApi) -> GetUserInformationResponseApi:
        get_user_information_request = self._mapper(get_user_information_request_api, GetUserInformationRequest)
        get_user_information_result = self._user_information_service_processor.get_user_information(get_user_information_request)
        return self._mapper(get_user_information_result, GetUserInformationResponseApi)
