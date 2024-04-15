from services.frontend_server.configuration.frontend_server_configuration_base import FrontendServerConfigurationBase


class FrontendServerConfigurationTest(FrontendServerConfigurationBase):
    SERVER_NAME = 'localhost:40000'
    PREFERRED_URL_SCHEME = 'http'