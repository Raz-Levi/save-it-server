from abc import ABC, abstractmethod


class AuthenticationPreferencesInterface(ABC):
    @property
    @abstractmethod
    def min_password_length(self):
        pass

    @property
    @abstractmethod
    def password_must_lowercase(self):
        pass

    @property
    @abstractmethod
    def password_must_uppercase(self):
        pass

    @property
    @abstractmethod
    def password_must_digit(self):
        pass

    @property
    @abstractmethod
    def password_must_special_char(self):
        pass


class AuthenticationPreferences(AuthenticationPreferencesInterface):
    @property
    def min_password_length(self):
        return 6

    @property
    def password_must_lowercase(self):
        return False

    @property
    def password_must_uppercase(self):
        return False

    @property
    def password_must_digit(self):
        return False

    @property
    def password_must_special_char(self):
        return False
