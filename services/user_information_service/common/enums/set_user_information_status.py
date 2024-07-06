from enum import Enum


class SetUserInformationStatus(Enum):
    SUCCESS = 0
    INVALID_USER_ID = 1
    INVALID_NAME = 2
    INVALID_EMAIL = 3
    INVALID_PHONE = 4
    UNKNOWN_ERROR = 5
