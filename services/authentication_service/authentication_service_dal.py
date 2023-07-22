import requests
import authentication_service_config as config


def register_user(email, password):
    url = config.AuthenticationConfigurations.get_signup_url()
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    data = response.json()
    return data


def login_user(email, password):
    url = config.AuthenticationConfigurations.get_signin_password_url()
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    data = response.json()
    return data


def authentication_init():
    email = "qa@qa.qa"
    password = "qaqaqa"

    # Register a new user
    registration_response = register_user(email, password)
    print("Registration Response:", registration_response)

    # Log in an existing user
    login_response = login_user(email, password)
    print("Login Response:", login_response)


if __name__ == '__main__':
    authentication_init()
