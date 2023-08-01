import pytest
from pytest_mock import MockerFixture
from requests import Response
from services.authentication_service.core.repositories.authentication_repository import AuthenticationRepository
from common.interface.communication_interface import CommunicationInterface
from services.authentication_service.core.configurations.authentication_service_config import AuthenticationConfigurationsInterface
from services.authentication_service.core.models.dal.dal_authentication_response import DalAuthenticationResponse
from services.authentication_service.client.enums.email_sign_up_status import EmailSignUpStatus


class TestAuthenticationRepository:
    @pytest.fixture(autouse=True)
    def setup_data(self, mocker: MockerFixture):
        self.communication = mocker.MagicMock(CommunicationInterface)
        self.configurations = mocker.MagicMock(AuthenticationConfigurationsInterface)

        self.authentication_repository = AuthenticationRepository(self.communication, self.configurations)

    def test_register_new_user_email_success(self, mocker: MockerFixture):
        # Arrange
        email = 'john@example.com'
        password = "qaqaqa"
        id_token = 123
        signup_url = "abc"

        response_mock = mocker.MagicMock(Response)
        response_mock.json.return_value = {'idToken': id_token}
        self.communication.post.return_value = lambda url, json: response_mock
        self.configurations.get_signup_url.return_value = signup_url

        # Act
        response = self.authentication_repository.register_new_user_email(email, password)

        # Assert
        assert type(response) == DalAuthenticationResponse
        assert response.is_success == True
        assert response.status == EmailSignUpStatus.SUCCESS
        assert response.id_token == id_token

    def test_register_new_user_email_email_exists(self, mocker: MockerFixture):
        # Arrange
        email = 'john@example.com'
        password = "qaqaqa"
        signup_url = "abc"

        response_mock = mocker.MagicMock(Response)
        response_mock.json.return_value = {'error': {'message': "EMAIL_EXISTS"}}
        self.communication.post.return_value = lambda url, json: response_mock
        self.configurations.get_signup_url.return_value = signup_url

        # Act
        response = self.authentication_repository.register_new_user_email(email, password)

        # Assert
        assert type(response) == DalAuthenticationResponse
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.EMAIL_EXISTS
        assert response.id_token is None

    def test_register_new_user_email_unknown_error(self, mocker: MockerFixture):
        # Arrange
        email = 'john@example.com'
        password = "qaqaqa"
        signup_url = "abc"

        response_mock = mocker.MagicMock(Response)
        response_mock.json.return_value = {}
        self.communication.post.return_value = lambda url, json: response_mock
        self.configurations.get_signup_url.return_value = signup_url

        # Act
        response = self.authentication_repository.register_new_user_email(email, password)

        # Assert
        assert type(response) == DalAuthenticationResponse
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.UNKNOWN_ERROR
        assert response.id_token is None
