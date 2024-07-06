from enum import Enum


class GetUserInformationStatus(Enum):
    SUCCESS = 0
    USER_ID_NOT_FOUND = 1
    UNKNOWN_ERROR = 2
