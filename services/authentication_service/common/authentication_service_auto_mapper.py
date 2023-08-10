from common.interface.auto_mapper_interface import AutoMapperInterface
from common.objects.auto_mapper_config import AutoMapperConfig
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.core.models.sign_up.sign_up_request import EmailSignUpRequest
from services.authentication_service.client.api.sign_up.sign_up_response_api import EmailSignUpResponseApi
from services.authentication_service.core.models.sign_up.sign_up_response import EmailSignUpResponse
from services.authentication_service.core.models.dal.dal_authentication_response import DalAuthenticationResponse
from services.authentication_service.core.models.checklivestatus.authentication_check_live_status_response import AuthenticationCheckLiveStatusResponse
from services.authentication_service.client.api.checklivestatus.authentication_check_live_status_response_api import AuthenticationCheckLiveStatusResponseApi
from services.frontend_server.core.models.sign_up.frontend_server_sign_up_response import FrontendServerEmailSignUpResponse


class AuthenticationServiceAutoMapper(AutoMapperInterface):
    @property
    def mapping_config(self):
        return [
            AutoMapperConfig(EmailSignUpRequestApi, EmailSignUpRequest),
            AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
            AutoMapperConfig(EmailSignUpResponse, EmailSignUpResponseApi),
            AutoMapperConfig(AuthenticationCheckLiveStatusResponse, AuthenticationCheckLiveStatusResponseApi),
            AutoMapperConfig(EmailSignUpResponseApi, FrontendServerEmailSignUpResponse),
        ]
