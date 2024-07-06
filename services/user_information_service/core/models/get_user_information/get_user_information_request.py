from dataclasses import dataclass


@dataclass
class GetUserInformationRequest:
    user_id: str
