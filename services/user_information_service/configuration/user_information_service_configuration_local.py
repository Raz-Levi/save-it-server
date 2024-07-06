from services.user_information_service.configuration.user_information_service_configuration_base import UserInformationServiceConfigurationBase


class UserInformationServiceConfigurationLocal(UserInformationServiceConfigurationBase):
    SERVER_NAME = 'localhost:4040'
    PREFERRED_URL_SCHEME = 'http'
