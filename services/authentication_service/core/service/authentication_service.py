import argparse
from common.enums.environment_configuration import EnvironmentConfiguration
from common.interface.service_interface import ServiceInterface
from flask import request, Response
from injector import inject
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.common.authentication_service_injector import AuthenticationServiceInjector
from services.authentication_service.configuration.authentication_service_configuration_factory import AuthenticationServiceConfigurationFactory
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
        email_sign_up_request_api_model = self._api.model('EmailSignUpRequestApi', {
            'email': fields.String(required=True, description="User's Email Address"),
            'password': fields.String(required=True, description="User's Password")
        })

        @self._maintenance_namespace.route('/checklivestatus')
        class CheckLiveStatusResource(Resource):
            @staticmethod
            def post() -> Response:
                result = self._authentication_service_controller.checklivestatus()
                return self.stringify_result(result)

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
    parser = argparse.ArgumentParser(description='Run authentication service according to the configurations')
    parser.add_argument('--env', type=EnvironmentConfiguration, help='The environment that the service run in', choices=list(EnvironmentConfiguration), default=EnvironmentConfiguration.LOCAL)
    args = parser.parse_args()

    authentication_service_configuration_factory = AuthenticationServiceConfigurationFactory()
    AuthenticationServiceInjector(args.env).inject(AuthenticationService).run_service(authentication_service_configuration_factory(args.env))
