class UserInformationServiceConfigurationBase:
    DEBUG = False
    TESTING = True
    SERVER_NAME = 'localhost:4040'
    PREFERRED_URL_SCHEME = 'http'

    @property
    def full_server_url(self):
        return f'{self.PREFERRED_URL_SCHEME}://{self.SERVER_NAME}'
