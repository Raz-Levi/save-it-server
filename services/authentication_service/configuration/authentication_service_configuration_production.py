from services.authentication_service.configuration.authentication_service_configuration_base import AuthenticationServiceConfigurationBase


class AuthenticationServiceConfigurationProduction(AuthenticationServiceConfigurationBase):
    DEBUG = False
    TESTING = False
    SERVER_NAME = 'localhost:40000'
    PREFERRED_URL_SCHEME = 'http'
