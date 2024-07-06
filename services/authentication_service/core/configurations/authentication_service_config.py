from hidden_files.authentication import authentication
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

    @property
    def signup_url(self) -> str:
        return f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={AuthenticationConfigurations._APP_KEY_API}"

    @property
    def login_url(self) -> str:
        return f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={AuthenticationConfigurations._APP_KEY_API}"
