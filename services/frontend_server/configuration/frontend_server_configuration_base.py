class FrontendServerConfigurationBase:
    DEBUG = False
    TESTING = False
    SERVER_NAME = 'localhost:40000'
    PREFERRED_URL_SCHEME = 'http'

    @property
    def full_server_url(self):
        return f'{self.PREFERRED_URL_SCHEME}://{self.SERVER_NAME}'
