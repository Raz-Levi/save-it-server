from dataclasses import dataclass
from services.user_information_service.common.enums.get_user_information_status import GetUserInformationStatus


@dataclass
class GetUserInformationResponse:
    is_success: bool
    user_id: str | None
    email: str | None
    full_name: str | None
    phone: str | None
    status: GetUserInformationStatus
