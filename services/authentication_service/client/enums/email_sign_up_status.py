from enum import Enum


class EmailSignUpStatus(Enum):
    SUCCESS = 0
    EMAIL_EXISTS = 1
    UNKNOWN_ERROR = 2
