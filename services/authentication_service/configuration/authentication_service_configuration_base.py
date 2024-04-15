class AuthenticationServiceConfigurationBase:
    DEBUG = False
    TESTING = True
    SERVER_NAME = 'localhost:8080'
    PREFERRED_URL_SCHEME = 'http'

    @property
    def full_server_url(self):
        return f'{self.PREFERRED_URL_SCHEME}://{self.SERVER_NAME}'
