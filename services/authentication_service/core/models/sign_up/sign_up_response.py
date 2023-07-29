from dataclasses import dataclass


@dataclass
class EmailSignUpResponse:
    is_success: bool
    error_message: str | None = None
