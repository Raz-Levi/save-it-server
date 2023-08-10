from abc import ABC, abstractmethod
from injector import inject
from common.interface.auto_mapper_interface import AutoMapperInterface
from services.frontend_server.client.api.sign_up.frontend_server_sign_up_request_api import FrontendServerEmailSignUpRequestApi
from services.frontend_server.client.api.sign_up.frontend_server_sign_up_response_api import FrontendServerEmailSignUpResponseApi
from services.frontend_server.core.models.sign_up.frontend_server_sign_up_request import FrontendServerEmailSignUpRequest
from services.frontend_server.core.processor.frontend_server_processor import FrontendServerProcessorInterface
from services.frontend_server.client.api.checklivestatus.frontend_check_live_status_response_api import FrontendServerCheckLiveStatusResponseApi


class FrontendServerControllerInterface(ABC):
    @abstractmethod
    def checklivestatus(self) -> FrontendServerCheckLiveStatusResponseApi:
        pass

    @abstractmethod
    def email_sign_up(self, email_signup_request_api: FrontendServerEmailSignUpRequestApi) -> FrontendServerEmailSignUpResponseApi:
        pass

    @abstractmethod
    def email_login(self, email_signup_request_api: FrontendServerEmailSignUpRequestApi) -> FrontendServerEmailSignUpResponseApi:
        pass


class FrontendServerController(FrontendServerControllerInterface):
    @inject
    def __init__(self, mapper: AutoMapperInterface, frontend_server_processor: FrontendServerProcessorInterface):
        self._mapper = mapper
        self._frontend_server_processor = frontend_server_processor

    def checklivestatus(self) -> FrontendServerCheckLiveStatusResponseApi:
        check_live_status_response = self._frontend_server_processor.checklivestatus()
        return self._mapper(check_live_status_response, FrontendServerCheckLiveStatusResponseApi)

    def email_sign_up(self, frontend_server_email_signup_request_api: FrontendServerEmailSignUpRequestApi) -> FrontendServerEmailSignUpResponseApi:
        frontend_server_email_signup_request = self._mapper(frontend_server_email_signup_request_api, FrontendServerEmailSignUpRequest)
        frontend_server_email_signup_response = self._frontend_server_processor.email_sign_up(frontend_server_email_signup_request)
        return self._mapper(frontend_server_email_signup_response, FrontendServerEmailSignUpResponseApi)

    def email_login(self, frontend_server_email_signup_request_api: FrontendServerEmailSignUpRequestApi) -> FrontendServerEmailSignUpResponseApi:
        frontend_server_email_signup_request = self._mapper(frontend_server_email_signup_request_api, FrontendServerEmailSignUpRequest)
        frontend_server_email_signup_response = self._frontend_server_processor.email_login(frontend_server_email_signup_request)
        return self._mapper(frontend_server_email_signup_response, FrontendServerEmailSignUpResponseApi)
