import argparse
from common.enums.environment_configuration import EnvironmentConfiguration
from common.interface.service_interface import ServiceInterface
from flask import request, Response
from injector import inject
from flask_restx import Resource, fields
from services.user_information_service.client.api.get_user_information.get_user_information_request_api import GetUserInformationRequestApi
from services.user_information_service.client.api.set_user_information.set_user_information_request_api import SetUserInformationRequestApi
from services.user_information_service.common.user_information_service_injector import UserInformationServiceInjector
from services.user_information_service.configuration.user_information_service_configuration_factory import UserInformationServiceConfigurationFactory
from services.user_information_service.core.controller.user_information_service_controller import UserInformationServiceControllerInterface


class UserInformationService(ServiceInterface):
    @inject
    def __init__(self, user_information_service_controller: UserInformationServiceControllerInterface):
        self._user_information_service_controller = user_information_service_controller
        self._user_information_namespace = self.define_namespace(namespace_name='user_information', description='User Information Related Requests')

        super().__init__()
        self._api.add_namespace(self._user_information_namespace)

    @property
    def service_name(self) -> str:
        return "user_information"

    def define_routes(self) -> None:
        set_user_information_request_api_model = self._api.model('SetUserInformationRequestApi', {
            'user_id': fields.String(required=True, description="User's ID"),
            'email': fields.String(required=True, description="User's email address"),
            'full_name': fields.String(required=True, description="User's full name"),
            'phone': fields.String(required=True, description="User's phone number")
        })

        get_user_information_request_api_model = self._api.model('GetUserInformationRequestApi', {
            'user_id': fields.String(required=True, description="User's ID"),
        })

        @self._maintenance_namespace.route('/checklivestatus')
        class CheckLiveStatusResource(Resource):
            @staticmethod
            def post() -> Response:
                result = self._user_information_service_controller.checklivestatus()
                return self.stringify_result(result)

        @self._user_information_namespace.route('/set_user_information')
        class SetUserInformationResource(Resource):
            @staticmethod
            @self._api.expect(set_user_information_request_api_model)
            def post() -> Response:
                data = request.json
                set_user_information_request_api = SetUserInformationRequestApi(data['user_id'], data['email'], data['full_name'], data['phone'])
                result = self._user_information_service_controller.set_user_information(set_user_information_request_api)
                return self.stringify_result(result)

        @self._user_information_namespace.route('/get_user_information')
        class GetUserInformationResource(Resource):
            @staticmethod
            @self._api.expect(get_user_information_request_api_model)
            def post() -> Response:
                data = request.json
                get_user_information_request_api = GetUserInformationRequestApi(data['user_id'])
                result = self._user_information_service_controller.get_user_information(get_user_information_request_api)
                return self.stringify_result(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run user information service according to the configurations')
    parser.add_argument('--env', type=EnvironmentConfiguration, help='The environment that the service run in', choices=list(EnvironmentConfiguration), default=EnvironmentConfiguration.LOCAL)
    args = parser.parse_args()

    user_information_service_configuration_factory = UserInformationServiceConfigurationFactory()
    UserInformationServiceInjector(args.env).inject(UserInformationService).run_service(user_information_service_configuration_factory(args.env))
