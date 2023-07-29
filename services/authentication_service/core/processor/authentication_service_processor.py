from injector import inject
from services.authentication_service.core.models.sign_up.sign_up_request import EmailSignUpRequest
from services.authentication_service.core.models.sign_up.sign_up_response import EmailSignUpResponse
from services.authentication_service.core.repositories.authentication_repository import AuthenticationRepository


class AuthenticationServiceProcessor:
    @inject
    def __init__(self, authentication_repository: AuthenticationRepository):
        self.authentication_repository = authentication_repository

    def email_sign_up(self, email_sign_up_request: EmailSignUpRequest) -> EmailSignUpResponse:
        response = self.authentication_repository.register_new_user_email(email_sign_up_request.email, email_sign_up_request.password)
        return EmailSignUpResponse(True)  # TODO- create EmailSignUpResponse from the response
