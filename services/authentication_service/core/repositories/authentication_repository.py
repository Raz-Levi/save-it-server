from injector import inject
from common.interface.communication_interface import CommunicationInterface
from services.authentication_service.core.configurations.authentication_service_config import AuthenticationConfigurations


class AuthenticationRepository:
    @inject
    def __init__(self, communication: CommunicationInterface, configurations: AuthenticationConfigurations):
        self.communication = communication
        self.configurations = configurations

    def register_new_user_email(self, email, password):  # TODO- annotate
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = self.communication.post(self.configurations.get_signup_url(), json=payload)
        data = response.json()
        return data

    def login_user_email(self, email, password):
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = self.communication.post(self.configurations.get_signup_url(), json=payload)
        data = response.json()
        return data



# def authentication_init():  #TODO- use it as a test
#     email = "qa@qa.qa"
#     password = "qaqaqa"
#
#     # Register a new user
#     registration_response = register_user(email, password)
#     print("Registration Response:", registration_response)
#
#     # Log in an existing user
#     login_response = login_user(email, password)
#     print("Login Response:", login_response)
#
#
# if __name__ == '__main__':
#     authentication_init()
