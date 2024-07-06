from dataclasses import dataclass
from services.user_information_service.core.models.dal.user_information.dal_user_information import DalUserInformation


@dataclass
class DalGetUserInformationResponse:
    is_success: bool
    dal_user_information: DalUserInformation | None
