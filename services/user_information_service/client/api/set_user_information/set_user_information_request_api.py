from dataclasses import dataclass


@dataclass
class SetUserInformationRequestApi:
    user_id: str
    email: str
    full_name: str
    phone: str
