from dataclasses import dataclass


@dataclass
class EmailSignUpResponseApi:
    is_success: bool
    error_message: str | None
