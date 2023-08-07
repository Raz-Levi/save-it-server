from dataclasses import dataclass


@dataclass
class FrontendServerEmailSignUpRequestApi:
    email: str
    password: str
