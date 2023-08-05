from common.interface.service_interface import ServiceInterface
from flask import request, Response
from injector import inject
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.common.authentication_service_injector import AuthenticationServiceInjector
from services.authentication_service.core.controller.authentication_service_controller import AuthenticationServiceControllerInterface


class AuthenticationService(ServiceInterface):
    @inject
    def __init__(self, authentication_service_controller: AuthenticationServiceControllerInterface):
        self.authentication_service_controller = authentication_service_controller
        super().__init__()

    @property
    def get_service_name(self) -> str:
        return "authentication_service"

    def define_routes(self) -> None:
        super().define_routes()

        @self.app.route(f"/{self.get_service_name}/sign_up", methods=['POST'])
        def signup() -> Response:
            data = request.json
            email_signup_request_api = EmailSignUpRequestApi(data['email'], data['password'])
            result = self.authentication_service_controller.email_sign_up(email_signup_request_api)
            return self.stringify_result(result)


if __name__ == "__main__":
    AuthenticationServiceInjector.inject(AuthenticationService).run_service(8080)
