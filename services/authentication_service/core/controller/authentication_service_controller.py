from injector import inject
from services.authentication_service.common.authentication_service_auto_mapper import AuthenticationServiceAutoMapper
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.client.api.sign_up.sign_up_response_api import EmailSignUpResponseApi
from services.authentication_service.core.processor.authentication_service_processor import AuthenticationServiceProcessor
from services.authentication_service.core.models.sign_up.sign_up_request import EmailSignUpRequest


class AuthenticationServiceController:
    @inject
    def __init__(self, mapper: AuthenticationServiceAutoMapper, authentication_service_processor: AuthenticationServiceProcessor):
        self.mapper = mapper
        self.authentication_service_processor = authentication_service_processor

    def email_sign_up(self, email_sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:
        email_sign_up_request = self.mapper(email_sign_up_request_api, EmailSignUpRequest)
        email_sign_up_result = self.authentication_service_processor.email_sign_up(email_sign_up_request)
        return self.mapper(email_sign_up_result, EmailSignUpResponseApi)
