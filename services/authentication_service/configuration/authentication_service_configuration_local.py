from services.authentication_service.configuration.authentication_service_configuration_base import AuthenticationServiceConfigurationBase


class AuthenticationServiceConfigurationLocal(AuthenticationServiceConfigurationBase):
    SERVER_NAME = 'localhost:8080'
    PREFERRED_URL_SCHEME = 'http'
