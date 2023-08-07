from dataclasses import dataclass


@dataclass
class FrontendServerEmailSignUpRequest:
    email: str
    password: str
