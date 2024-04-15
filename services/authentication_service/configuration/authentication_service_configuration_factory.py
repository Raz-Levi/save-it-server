from common.enums.environment_configuration import EnvironmentConfiguration
from services.authentication_service.configuration.authentication_service_configuration_base import AuthenticationServiceConfigurationBase
from services.authentication_service.configuration.authentication_service_configuration_local import AuthenticationServiceConfigurationLocal
from services.authentication_service.configuration.authentication_service_configuration_production import AuthenticationServiceConfigurationProduction
from services.authentication_service.configuration.authentication_service_configuration_test import AuthenticationServiceConfigurationTest


class AuthenticationServiceConfigurationFactory:
    def __call__(self, environment_configuration_name: EnvironmentConfiguration) -> AuthenticationServiceConfigurationBase:
        match environment_configuration_name:
            case EnvironmentConfiguration.TEST:
                return AuthenticationServiceConfigurationTest()

            case EnvironmentConfiguration.PRODUCTION:
                return AuthenticationServiceConfigurationProduction()

            case _:
                return AuthenticationServiceConfigurationLocal()
