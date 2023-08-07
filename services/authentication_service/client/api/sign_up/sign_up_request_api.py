from dataclasses import dataclass


@dataclass
class EmailSignUpRequestApi:
    email: str
    password: str
