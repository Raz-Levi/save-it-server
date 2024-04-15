from common.enums.environment_configuration import EnvironmentConfiguration
from services.frontend_server.configuration.frontend_server_configuration_base import FrontendServerConfigurationBase
from services.frontend_server.configuration.frontend_server_configuration_local import FrontendServerConfigurationLocal
from services.frontend_server.configuration.frontend_server_configuration_production import FrontendServerConfigurationProduction
from services.frontend_server.configuration.frontend_server_configuration_test import FrontendServerConfigurationTest


class FrontendServerConfigurationFactory:
    def __call__(self, environment_configuration_name: EnvironmentConfiguration):
        match environment_configuration_name:
            case EnvironmentConfiguration.TEST:
                return FrontendServerConfigurationTest

            case EnvironmentConfiguration.PRODUCTION:
                return FrontendServerConfigurationProduction

            case _:
                return FrontendServerConfigurationLocal
