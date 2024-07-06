from dataclasses import dataclass


@dataclass
class GetUserInformationResponseApi:
    is_success: bool
    user_id: str | None
    email: str | None
    full_name: str | None
    phone: str | None
