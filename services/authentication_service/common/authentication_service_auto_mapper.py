from common.interface.auto_mapper_interface import AutoMapperInterface
from common.objects.auto_mapper_config import AutoMapperConfig
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.core.models.sign_up.sign_up_request import EmailSignUpRequest
from services.authentication_service.client.api.sign_up.sign_up_response_api import EmailSignUpResponseApi
from services.authentication_service.core.models.sign_up.sign_up_response import EmailSignUpResponse


class AuthenticationServiceAutoMapper(AutoMapperInterface):
    def __init__(self):
        super().__init__()
        self.mapping_config = [
            AutoMapperConfig(EmailSignUpRequestApi, EmailSignUpRequest),
            AutoMapperConfig(EmailSignUpResponseApi, EmailSignUpResponse),
        ]
