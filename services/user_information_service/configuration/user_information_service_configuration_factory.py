from common.enums.environment_configuration import EnvironmentConfiguration
from services.user_information_service.configuration.user_information_service_configuration_base import UserInformationServiceConfigurationBase
from services.user_information_service.configuration.user_information_service_configuration_local import UserInformationServiceConfigurationLocal
from services.user_information_service.configuration.user_information_service_configuration_production import UserInformationServiceConfigurationProduction
from services.user_information_service.configuration.user_information_service_configuration_test import UserInformationServiceConfigurationTest


class UserInformationServiceConfigurationFactory:
    def __call__(self, environment_configuration_name: EnvironmentConfiguration) -> UserInformationServiceConfigurationBase:
        match environment_configuration_name:
            case EnvironmentConfiguration.TEST:
                return UserInformationServiceConfigurationTest()

            case EnvironmentConfiguration.PRODUCTION:
                return UserInformationServiceConfigurationProduction()

            case _:
                return UserInformationServiceConfigurationLocal()
