from injector import inject, Injector
from services.authentication_service.core.controller.authentication_service_controller import AuthenticationServiceController
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.client.api.sign_up.sign_up_response_api import EmailSignUpResponseApi


class AuthenticationServiceClient:
    @inject
    def __init__(self, authentication_service_controller: AuthenticationServiceController):
        self._authentication_service_controller = authentication_service_controller

    @staticmethod
    def get_instance():
        injector = Injector(lambda binder: binder.bind(AuthenticationServiceController, to=AuthenticationServiceController()))
        new_authentication_service_client = injector.get(AuthenticationServiceClient)
        new_authentication_service_client._authentication_service_controller = AuthenticationServiceController()
        return new_authentication_service_client

    def sign_up(self, sign_up_request_api: EmailSignUpRequestApi) -> EmailSignUpResponseApi:  # TODO- implement REST
        return self._authentication_service_controller.sign_up(sign_up_request_api)
