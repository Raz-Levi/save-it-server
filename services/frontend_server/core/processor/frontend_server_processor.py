from abc import ABC, abstractmethod
from injector import inject
from common.interface.auto_mapper_interface import AutoMapperInterface
from services.frontend_server.core.models.sign_up.frontend_server_sign_up_request import \
    FrontendServerEmailSignUpRequest
from services.frontend_server.core.models.sign_up.frontend_server_sign_up_response import \
    FrontendServerEmailSignUpResponse
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.client.client_api.authentication_service_client import \
    AuthenticationServiceClientInterface
from services.frontend_server.core.models.checklivestatus.frontend_check_live_status_response import \
    FrontendServerCheckLiveStatusResponse
from common.enums.server_live_status import ServerLiveStatus


class FrontendServerProcessorInterface(ABC):
    def checklivestatus(self) -> FrontendServerCheckLiveStatusResponse:
        pass

    @abstractmethod
    def email_sign_up(self,
                      frontend_server_email_signup_request: FrontendServerEmailSignUpRequest) -> FrontendServerEmailSignUpResponse:
        pass

    @abstractmethod
    def email_login(self,
                    frontend_server_email_signup_request: FrontendServerEmailSignUpRequest) -> FrontendServerEmailSignUpResponse:
        pass


class FrontendServerProcessor(FrontendServerProcessorInterface):
    @inject
    def __init__(self, mapper: AutoMapperInterface, authentication_service_client: AuthenticationServiceClientInterface):
        self._mapper = mapper
        self._authentication_service_client = authentication_service_client

    def checklivestatus(self) -> FrontendServerCheckLiveStatusResponse:
        response = FrontendServerCheckLiveStatusResponse(frontend_server_status=ServerLiveStatus.ALIVE)

        try:
            response.authentication_service_status = self._authentication_service_client.checklivestatus().status
        except:
            response.authentication_service_status = ServerLiveStatus.DEAD

        return response

    def email_sign_up(self,
                      frontend_server_email_signup_request: FrontendServerEmailSignUpRequest) -> FrontendServerEmailSignUpResponse:
        email_signup_request_api = self._mapper(frontend_server_email_signup_request, EmailSignUpRequestApi)
        email_signup_response_api = self._authentication_service_client.email_sign_up(email_signup_request_api)
        return self._mapper(email_signup_response_api, FrontendServerEmailSignUpResponse)

    def email_login(self,
                    frontend_server_email_signup_request: FrontendServerEmailSignUpRequest) -> FrontendServerEmailSignUpResponse:
        email_signup_request_api = self._mapper(frontend_server_email_signup_request, EmailSignUpRequestApi)
        email_signup_response_api = self._authentication_service_client.email_login(email_signup_request_api)
        return self._mapper(email_signup_response_api, FrontendServerEmailSignUpResponse)
