from injector import inject
import email_validator
import phonenumbers
from abc import ABC, abstractmethod
from common.interface.auto_mapper_interface import AutoMapperInterface
from common.enums.server_live_status import ServerLiveStatus
from common.objects.logger import LoggerInterface
from services.user_information_service.core.models.checklivestatus.user_information_check_live_status_response import UserInformationCheckLiveStatusResponse
from services.user_information_service.core.models.dal.user_information.dal_user_information import DalUserInformation
from services.user_information_service.core.models.get_user_information.get_user_information_request import GetUserInformationRequest
from services.user_information_service.core.models.get_user_information.get_user_information_response import GetUserInformationResponse
from services.user_information_service.core.models.set_user_information.set_user_information_request import SetUserInformationRequest
from services.user_information_service.core.models.set_user_information.set_user_information_response import SetUserInformationResponse
from services.user_information_service.core.repositories.user_information_repository import UserInformationRepositoryInterface


class UserInformationServiceProcessorInterface(ABC):
    @abstractmethod
    def checklivestatus(self) -> UserInformationCheckLiveStatusResponse:
        pass

    @abstractmethod
    def set_user_information(self, set_user_information_request: SetUserInformationRequest) -> SetUserInformationResponse:
        pass

    @abstractmethod
    def get_user_information(self, get_user_information_request: GetUserInformationRequest) -> GetUserInformationResponse:
        pass


class UserInformationServiceProcessor(UserInformationServiceProcessorInterface):
    @inject
    def __init__(self, mapper: AutoMapperInterface, logger: LoggerInterface, user_information_repository: UserInformationRepositoryInterface):
        self._mapper = mapper
        self._logger = logger
        self._user_information_repository = user_information_repository

    def checklivestatus(self) -> UserInformationCheckLiveStatusResponse:
        return UserInformationCheckLiveStatusResponse(ServerLiveStatus.ALIVE)

    def set_user_information(self, set_user_information_request: SetUserInformationRequest) -> SetUserInformationResponse:
        # TODO- add validation status to the response
        try:
            if email_validator.validate_email(set_user_information_request.email) is False:
                self._logger.warning(f"Invalid email address: {set_user_information_request.email}")
                return SetUserInformationResponse(is_success=False)

        except Exception as e:
            self._logger.warning(f"Invalid email address: {set_user_information_request.email}")
            return SetUserInformationResponse(is_success=False)

        try:
            if self._is_valid_name(set_user_information_request.full_name) is False:
                self._logger.warning(f"Invalid name: {set_user_information_request.full_name}")
                return SetUserInformationResponse(is_success=False)

            if phonenumbers.is_valid_number(phonenumbers.parse(set_user_information_request.phone, "IL")) is False:  # TODO- change the country code to a configuration
                self._logger.warning(f"Invalid phone number: {set_user_information_request.phone}")
                return SetUserInformationResponse(is_success=False)

        except Exception as e:
            self._logger.warning(f"Invalid phone number: {set_user_information_request.phone}")
            return SetUserInformationResponse(is_success=False)

        response = self._user_information_repository.set_user_information_by_user_id(set_user_information_request.user_id, self._mapper(set_user_information_request, DalUserInformation))
        return self._mapper(response, SetUserInformationResponse)

    def get_user_information(self, get_user_information_request: GetUserInformationRequest) -> GetUserInformationResponse:
        response = self._user_information_repository.get_user_information_by_user_id(get_user_information_request.user_id)
        if response.is_success is True:
            return GetUserInformationResponse(is_success=response.is_success,
                                              user_id=response.dal_user_information.user_id,
                                              email=response.dal_user_information.email,
                                              full_name=response.dal_user_information.full_name,
                                              phone=response.dal_user_information.phone)

        return GetUserInformationResponse(is_success=False, user_id=None, email=None, full_name=None, phone=None)

    ############### Private ###############
    def _is_valid_name(self, name):
        first_space_index_in_name = name.find(' ')
        return name.replace(" ", "").isalpha() and first_space_index_in_name != -1 and first_space_index_in_name != 0 and name.rfind(" ") != len(name) - 1
