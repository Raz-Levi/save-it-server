from enum import Enum


class EmailSignUpStatus(Enum):
    SUCCESS = 0
    EMAIL_EXISTS = 1
    EMAIL_NOT_FOUND = 2
    UNKNOWN_ERROR = 3
