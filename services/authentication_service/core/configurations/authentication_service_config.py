from hidden_files import authentication
from abc import ABC, abstractmethod


class AuthenticationConfigurationsInterface(ABC):
    @property
    @abstractmethod
    def signup_url(self) -> str:
        pass

    @property
    @abstractmethod
    def login_url(self) -> str:
        pass


class AuthenticationConfigurations(AuthenticationConfigurationsInterface):
    _APP_KEY_API = authentication.APP_KEY_API
    _AUTHENTICATION_URL = authentication.AUTHENTICATION_URL

    @property
    def signup_url(self) -> str:
        return f"{AuthenticationConfigurations._AUTHENTICATION_URL}signUp?key={AuthenticationConfigurations._APP_KEY_API}"

    @property
    def login_url(self) -> str:
        return f"{AuthenticationConfigurations._AUTHENTICATION_URL}signInWithPassword?key={AuthenticationConfigurations._APP_KEY_API}"
