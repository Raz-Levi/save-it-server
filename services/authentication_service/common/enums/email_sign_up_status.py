from enum import Enum


class EmailSignUpStatus(Enum):
    SUCCESS = 0
    EMAIL_EXISTS = 1
    EMAIL_NOT_FOUND = 2
    INVALID_PASSWORD = 3
    INVALID_EMAIL = 4
    UNKNOWN_ERROR = 5
