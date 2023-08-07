from common.configuration.server_configutrations.server_configurations_local import ServerConfigurationsLocal
from common.interface.service_interface import ServiceInterface
from flask import request, Response
from injector import inject
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.common.authentication_service_injector import AuthenticationServiceInjector
from services.authentication_service.core.controller.authentication_service_controller import AuthenticationServiceControllerInterface
from flask_restx import Resource, fields


class AuthenticationService(ServiceInterface):
    @inject
    def __init__(self, authentication_service_controller: AuthenticationServiceControllerInterface):
        self._authentication_service_controller = authentication_service_controller
        self._authentication_namespace = self.define_namespace(namespace_name='authentication', description='Authentication Related Requests')

        super().__init__()
        self._api.add_namespace(self._authentication_namespace)

    @property
    def service_name(self) -> str:
        return "authentication_service"

    def define_routes(self) -> None:
        super().define_routes()

        email_sign_up_request_api_model = self._api.model('EmailSignUpRequestApi', {
            'email': fields.String(required=True, description="User's Email Address"),
            'password': fields.String(required=True, description="User's Password")
        })

        @self._authentication_namespace.route('/email_sign_up')
        class EmailSignUpResource(Resource):
            @staticmethod
            @self._api.expect(email_sign_up_request_api_model)
            def post() -> Response:
                data = request.json
                email_signup_request_api = EmailSignUpRequestApi(data['email'], data['password'])
                result = self._authentication_service_controller.email_sign_up(email_signup_request_api)
                return self.stringify_result(result)

        @self._authentication_namespace.route('/email_login')
        class EmailLoginResource(Resource):
            @staticmethod
            @self._api.expect(email_sign_up_request_api_model)
            def post() -> Response:
                data = request.json
                email_signup_request_api = EmailSignUpRequestApi(data['email'], data['password'])
                result = self._authentication_service_controller.email_login(email_signup_request_api)
                return self.stringify_result(result)


if __name__ == '__main__':
    server_config = ServerConfigurationsLocal()  # TODO- update tp QA and Prod
    AuthenticationServiceInjector.inject(AuthenticationService).run_service(server_config.authentication_service_config.port)
