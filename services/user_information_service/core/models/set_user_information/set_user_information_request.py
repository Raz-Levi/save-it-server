from dataclasses import dataclass


@dataclass
class SetUserInformationRequest:
    user_id: str
    email: str
    full_name: str
    phone: str
