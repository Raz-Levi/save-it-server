from hidden_files import authentication
from abc import ABC


class AuthenticationConfigurationsInterface(ABC):
    @staticmethod
    def get_signup_url() -> str:
        pass

    @staticmethod
    def get_signin_password_url() -> str:
        pass


class AuthenticationConfigurations(AuthenticationConfigurationsInterface):
    _APP_KEY_API = authentication.APP_KEY_API
    _AUTHENTICATION_URL = authentication.AUTHENTICATION_URL

    @staticmethod
    def get_signup_url() -> str:
        return f"{AuthenticationConfigurations._AUTHENTICATION_URL}signUp?key={AuthenticationConfigurations._APP_KEY_API}"

    @staticmethod
    def get_signin_password_url() -> str:
        return f"{AuthenticationConfigurations._AUTHENTICATION_URL}signInWithPassword?key={AuthenticationConfigurations._APP_KEY_API}"
