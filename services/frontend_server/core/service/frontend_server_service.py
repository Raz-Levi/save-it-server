from common.configuration.server_configutrations.server_configurations_local import ServerConfigurationsLocal
from common.interface.service_interface import ServiceInterface
from flask import request, Response
from injector import inject
from services.frontend_server.client.api.frontend_server_sign_up_request_api import FrontendServerEmailSignUpRequestApi
from services.frontend_server.common.frontend_server_injector import FrontendServerInjector
from services.frontend_server.core.controller.frontend_server_controller import FrontendServerControllerInterface
from flask_restx import Resource, fields


class FrontendServer(ServiceInterface):
    @inject
    def __init__(self, frontend_server_controller: FrontendServerControllerInterface):
        self._frontend_server_controller = frontend_server_controller
        self._authentication_namespace = self.define_namespace(namespace_name='authentication', description='Authentication Related Requests')

        super().__init__()
        self._api.add_namespace(self._authentication_namespace)

    @property
    def service_name(self) -> str:
        return "frontend_server"

    def checklivestatus(self) -> dict:
        return self._frontend_server_controller.checklivestatus()

    def define_routes(self) -> None:
        super().define_routes()

        frontend_server_email_sign_up_request_api_model = self._api.model('FrontendServerEmailSignUpRequestApi', {
            'email': fields.String(required=True, description="User's Email Address"),
            'password': fields.String(required=True, description="User's Password")
        })

        @self._authentication_namespace.route('/email_sign_up')
        class EmailSignUpResource(Resource):
            @staticmethod
            @self._api.expect(frontend_server_email_sign_up_request_api_model)
            def post() -> Response:
                data = request.json
                email_signup_request_api = FrontendServerEmailSignUpRequestApi(data['email'], data['password'])
                result = self._frontend_server_controller.email_sign_up(email_signup_request_api)
                return self.stringify_result(result)

        @self._authentication_namespace.route('/email_login')
        class EmailLoginResource(Resource):
            @staticmethod
            @self._api.expect(frontend_server_email_sign_up_request_api_model)
            def post() -> Response:
                data = request.json
                email_signup_request_api = FrontendServerEmailSignUpRequestApi(data['email'], data['password'])
                result = self._frontend_server_controller.email_login(email_signup_request_api)
                return self.stringify_result(result)


if __name__ == '__main__':
    server_config = ServerConfigurationsLocal()  # TODO- update tp QA and Prod
    FrontendServerInjector.inject(FrontendServer).run_service(server_config.frontend_server_config.port)
