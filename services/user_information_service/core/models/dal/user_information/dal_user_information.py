from dataclasses import dataclass


@dataclass
class DalUserInformation:
    user_id: str
    email: str
    full_name: str
    phone: str
