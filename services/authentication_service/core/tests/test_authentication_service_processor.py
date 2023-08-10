import pytest
from pytest_mock import MockerFixture
from services.authentication_service.core.repositories.authentication_repository import AuthenticationRepositoryInterface
from common.enums.server_live_status import ServerLiveStatus
from services.authentication_service.common.enums.email_sign_up_status import EmailSignUpStatus
from services.authentication_service.core.configurations.authentication_preferences import AuthenticationPreferencesInterface
from services.authentication_service.core.processor.authentication_service_processor import AuthenticationServiceProcessor
from common.interface.auto_mapper_interface import AutoMapperInterface
from common.objects.auto_mapper_config import AutoMapperConfig
from services.authentication_service.core.models.sign_up.sign_up_request import EmailSignUpRequest
from services.authentication_service.core.models.sign_up.sign_up_response import EmailSignUpResponse
from services.authentication_service.core.models.dal.dal_authentication_response import DalAuthenticationResponse
from services.authentication_service.core.models.checklivestatus.authentication_check_live_status_response import AuthenticationCheckLiveStatusResponse


class TestAuthenticationServiceProcessor:
    @pytest.fixture(autouse=True)
    def setup_data(self, mocker: MockerFixture):
        self._mapper = mocker.MagicMock(AutoMapperInterface)
        self._authentication_repository = mocker.MagicMock(AuthenticationRepositoryInterface)
        self._authentication_preferences = mocker.MagicMock(AuthenticationPreferencesInterface)

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

    def test_checklivestatus_success(self):
        # Act
        response = self._authentication_service_processor.checklivestatus()

        # Assert
        assert type(response) == AuthenticationCheckLiveStatusResponse
        assert response.status == ServerLiveStatus.ALIVE

    def test_email_sign_up_success(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('john@example.com', "qaqaqa")
        id_token = "id_token"

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return False

            @property
            def password_must_uppercase(self):
                return False

            @property
            def password_must_digit(self):
                return False

            @property
            def password_must_special_char(self):
                return False

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.register_new_user_email.return_value = DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_sign_up(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == True
        assert response.status == EmailSignUpStatus.SUCCESS
        assert response.id_token == id_token
        self._authentication_repository.register_new_user_email.assert_called_once()

    def test_email_sign_up_repository_email_sign_up_failure(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('john@example.com', "qaqaqa")

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return False

            @property
            def password_must_uppercase(self):
                return False

            @property
            def password_must_digit(self):
                return False

            @property
            def password_must_special_char(self):
                return False

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.register_new_user_email.return_value = DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.EMAIL_EXISTS)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_sign_up(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.EMAIL_EXISTS
        self._authentication_repository.register_new_user_email.assert_called_once()

    def test_email_sign_up_is_valid_email_failure(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('johnexample.com', "qaqaqa")
        id_token = "id_token"

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return False

            @property
            def password_must_uppercase(self):
                return False

            @property
            def password_must_digit(self):
                return False

            @property
            def password_must_special_char(self):
                return False

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.register_new_user_email.return_value = DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_sign_up(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.INVALID_EMAIL
        self._authentication_repository.register_new_user_email.assert_not_called()

    def test_email_sign_up_is_valid_email_and_is_valid_password_failure(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('johnexample.com', "q")
        id_token = "id_token"

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return False

            @property
            def password_must_uppercase(self):
                return False

            @property
            def password_must_digit(self):
                return False

            @property
            def password_must_special_char(self):
                return False

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.register_new_user_email.return_value = DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_sign_up(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.INVALID_EMAIL
        self._authentication_repository.register_new_user_email.assert_not_called()

    def test_email_sign_up_short_password_failure(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('john@example.com', "q")
        id_token = "id_token"

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return False

            @property
            def password_must_uppercase(self):
                return False

            @property
            def password_must_digit(self):
                return False

            @property
            def password_must_special_char(self):
                return False

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.register_new_user_email.return_value = DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_sign_up(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.INVALID_PASSWORD
        self._authentication_repository.register_new_user_email.assert_not_called()

    def test_email_sign_up_must_lowercase_password_failure(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('john@example.com', "QAQAQA")
        id_token = "id_token"

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return True

            @property
            def password_must_uppercase(self):
                return False

            @property
            def password_must_digit(self):
                return False

            @property
            def password_must_special_char(self):
                return False

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.register_new_user_email.return_value = DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_sign_up(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.INVALID_PASSWORD
        self._authentication_repository.register_new_user_email.assert_not_called()

    def test_email_sign_up_must_uppercase_password_failure(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('john@example.com', "qaqaqa")
        id_token = "id_token"

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return False

            @property
            def password_must_uppercase(self):
                return True

            @property
            def password_must_digit(self):
                return False

            @property
            def password_must_special_char(self):
                return False

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.register_new_user_email.return_value = DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_sign_up(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.INVALID_PASSWORD
        self._authentication_repository.register_new_user_email.assert_not_called()

    def test_email_sign_up_must_digit_password_failure(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('john@example.com', "qaqaqa")
        id_token = "id_token"

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return False

            @property
            def password_must_uppercase(self):
                return False

            @property
            def password_must_digit(self):
                return True

            @property
            def password_must_special_char(self):
                return False

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.register_new_user_email.return_value = DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_sign_up(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.INVALID_PASSWORD
        self._authentication_repository.register_new_user_email.assert_not_called()

    def test_email_sign_up_must_special_char_failure(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('john@example.com', "qaqaqa")
        id_token = "id_token"

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return False

            @property
            def password_must_uppercase(self):
                return False

            @property
            def password_must_digit(self):
                return False

            @property
            def password_must_special_char(self):
                return True

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.register_new_user_email.return_value = DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_sign_up(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.INVALID_PASSWORD
        self._authentication_repository.register_new_user_email.assert_not_called()

    def test_email_sign_up_strong_password_success(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('john@example.com', "qAqa2q#a")
        id_token = "id_token"

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return True

            @property
            def password_must_uppercase(self):
                return True

            @property
            def password_must_digit(self):
                return True

            @property
            def password_must_special_char(self):
                return True

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.register_new_user_email.return_value = DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_sign_up(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == True
        assert response.status == EmailSignUpStatus.SUCCESS
        assert response.id_token == id_token
        self._authentication_repository.register_new_user_email.assert_called_once()

    def test_email_login_success(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('john@example.com', "qaqaqa")
        id_token = "id_token"

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return True

            @property
            def password_must_uppercase(self):
                return True

            @property
            def password_must_digit(self):
                return True

            @property
            def password_must_special_char(self):
                return True

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.login_email.return_value = DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_login(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == True
        assert response.status == EmailSignUpStatus.SUCCESS
        assert response.id_token == id_token
        self._authentication_repository.login_email.assert_called_once()

    def test_email_login_repository_login_email_failure(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('john@example.com', "qaqaqa")

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return True

            @property
            def password_must_uppercase(self):
                return True

            @property
            def password_must_digit(self):
                return True

            @property
            def password_must_special_char(self):
                return True

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.login_email.return_value = DalAuthenticationResponse(is_success=False, status=EmailSignUpStatus.EMAIL_NOT_FOUND)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_login(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.EMAIL_NOT_FOUND
        self._authentication_repository.login_email.assert_called_once()

    def test_email_login_is_valid_email_failure(self):
        # Arrange
        email_sign_up_request = EmailSignUpRequest('johnexample.com', "qaqaqa")
        id_token = "id_token"

        class AuthenticationPreferences(AuthenticationPreferencesInterface):
            @property
            def min_password_length(self):
                return 6

            @property
            def password_must_lowercase(self):
                return True

            @property
            def password_must_uppercase(self):
                return True

            @property
            def password_must_digit(self):
                return True

            @property
            def password_must_special_char(self):
                return True

        self._authentication_preferences = AuthenticationPreferences()

        self._authentication_repository.login_email.return_value = DalAuthenticationResponse(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)

        class AuthenticationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalAuthenticationResponse, EmailSignUpResponse),
                ]

        self._mapper = AuthenticationServiceAutoMapper()

        self._authentication_service_processor = AuthenticationServiceProcessor(self._mapper, self._authentication_repository, self._authentication_preferences)

        # Act
        response = self._authentication_service_processor.email_login(email_sign_up_request)

        # Assert
        assert isinstance(response, EmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.INVALID_EMAIL
        self._authentication_repository.login_email.assert_not_called()
