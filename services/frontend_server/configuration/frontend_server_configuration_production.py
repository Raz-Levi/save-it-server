from services.frontend_server.configuration.frontend_server_configuration_base import FrontendServerConfigurationBase


class FrontendServerConfigurationProduction(FrontendServerConfigurationBase):
    DEBUG = False
    TESTING = False
    SERVER_NAME = 'localhost:40000'
    PREFERRED_URL_SCHEME = 'http'
