from dataclasses import dataclass
from services.user_information_service.common.enums.set_user_information_status import SetUserInformationStatus


@dataclass
class SetUserInformationResponseApi:
    is_success: bool
    status: SetUserInformationStatus
