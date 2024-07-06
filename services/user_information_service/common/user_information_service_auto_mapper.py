from common.interface.auto_mapper_interface import AutoMapperInterface
from common.objects.auto_mapper_config import AutoMapperConfig
from services.user_information_service.client.api.checklivestatus.user_information_check_live_status_response_api import UserInformationCheckLiveStatusResponseApi
from services.user_information_service.client.api.get_user_information.get_user_information_request_api import GetUserInformationRequestApi
from services.user_information_service.client.api.get_user_information.get_user_information_response_api import GetUserInformationResponseApi
from services.user_information_service.client.api.set_user_information.set_user_information_request_api import SetUserInformationRequestApi
from services.user_information_service.client.api.set_user_information.set_user_information_response_api import SetUserInformationResponseApi
from services.user_information_service.core.models.checklivestatus.user_information_check_live_status_response import UserInformationCheckLiveStatusResponse
from services.user_information_service.core.models.dal.user_information.dal_set_user_information_response import DalSetUserInformationDalResponse
from services.user_information_service.core.models.dal.user_information.dal_user_information import DalUserInformation
from services.user_information_service.core.models.get_user_information.get_user_information_request import GetUserInformationRequest
from services.user_information_service.core.models.get_user_information.get_user_information_response import GetUserInformationResponse
from services.user_information_service.core.models.set_user_information.set_user_information_request import SetUserInformationRequest
from services.user_information_service.core.models.set_user_information.set_user_information_response import SetUserInformationResponse


class UserInformationServiceAutoMapper(AutoMapperInterface):
    @property
    def mapping_config(self):
        return [
            AutoMapperConfig(GetUserInformationRequestApi, GetUserInformationRequest),
            AutoMapperConfig(SetUserInformationRequestApi, SetUserInformationRequest),
            AutoMapperConfig(SetUserInformationResponse, SetUserInformationResponseApi),
            AutoMapperConfig(GetUserInformationResponse, GetUserInformationResponseApi),
            AutoMapperConfig(UserInformationCheckLiveStatusResponse, UserInformationCheckLiveStatusResponseApi),
            AutoMapperConfig(SetUserInformationRequest, DalUserInformation),
            AutoMapperConfig(DalSetUserInformationDalResponse, SetUserInformationResponse),
        ]
