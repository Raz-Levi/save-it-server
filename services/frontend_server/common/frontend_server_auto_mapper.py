from common.interface.auto_mapper_interface import AutoMapperInterface
from common.objects.auto_mapper_config import AutoMapperConfig
from services.frontend_server.client.api.sign_up.frontend_server_sign_up_request_api import FrontendServerEmailSignUpRequestApi
from services.frontend_server.client.api.sign_up.frontend_server_sign_up_response_api import FrontendServerEmailSignUpResponseApi
from services.frontend_server.core.models.sign_up.frontend_server_sign_up_request import FrontendServerEmailSignUpRequest
from services.frontend_server.core.models.sign_up.frontend_server_sign_up_response import FrontendServerEmailSignUpResponse
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.client.api.sign_up.sign_up_response_api import EmailSignUpResponseApi


class FrontendServerAutoMapper(AutoMapperInterface):
    @property
    def mapping_config(self):
        return [
            AutoMapperConfig(FrontendServerEmailSignUpRequestApi, FrontendServerEmailSignUpRequest),
            AutoMapperConfig(FrontendServerEmailSignUpRequest, EmailSignUpRequestApi),
            AutoMapperConfig(EmailSignUpResponseApi, FrontendServerEmailSignUpResponse),
            AutoMapperConfig(FrontendServerEmailSignUpResponse, FrontendServerEmailSignUpResponseApi),
        ]
