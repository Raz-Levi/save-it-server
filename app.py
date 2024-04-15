import argparse
import threading
from common.enums.environment_configuration import EnvironmentConfiguration
from services.authentication_service.configuration.authentication_service_configuration_factory import AuthenticationServiceConfigurationFactory
from services.frontend_server.common.frontend_server_injector import FrontendServerInjector
from services.frontend_server.configuration.frontend_server_configuration_factory import FrontendServerConfigurationFactory
from services.frontend_server.core.service.frontend_server_service import FrontendServer
from services.authentication_service.common.authentication_service_injector import AuthenticationServiceInjector
from services.authentication_service.core.service.authentication_service import AuthenticationService


def run_frontend_server(environment_configuration: EnvironmentConfiguration) -> threading.Thread:
    frontend_server_configuration_factory = FrontendServerConfigurationFactory()
    return threading.Thread(target=lambda: FrontendServerInjector(environment_configuration).inject(FrontendServer).run_service(frontend_server_configuration_factory(environment_configuration)))


def run_authentication_service(environment_configuration: EnvironmentConfiguration) -> threading.Thread:
    authentication_service_configuration_factory = AuthenticationServiceConfigurationFactory()
    return threading.Thread(target=lambda: AuthenticationServiceInjector(environment_configuration).inject(AuthenticationService).run_service(authentication_service_configuration_factory(environment_configuration)))


def run_services_function() -> list:
    return [
        run_frontend_server,
        run_authentication_service
    ]


def run_all_services(environment_configuration: EnvironmentConfiguration):
    threads = [run_service_function(environment_configuration) for run_service_function in run_services_function()]
    for service in threads:
        service.start()

    for service in threads:
        service.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run all services according to the configurations')
    parser.add_argument('--env', type=EnvironmentConfiguration, help='The environment that the services run in', choices=list(EnvironmentConfiguration), default=EnvironmentConfiguration.LOCAL)
    args = parser.parse_args()

    run_all_services(args.env)

# TODO-
#  validations
#  logger and log4python
#  write tests for processors
#  create maintanance service that run all services together and separated
