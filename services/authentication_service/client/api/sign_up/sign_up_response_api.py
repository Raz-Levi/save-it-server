from dataclasses import dataclass
from services.authentication_service.client.enums.email_sign_up_status import EmailSignUpStatus


@dataclass
class EmailSignUpResponseApi:
    is_success: bool
    status: EmailSignUpStatus
    id_token: str | None = None
