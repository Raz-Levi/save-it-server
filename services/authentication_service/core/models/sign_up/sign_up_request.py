from dataclasses import dataclass


@dataclass
class EmailSignUpRequest:
    email: str
    password: str
