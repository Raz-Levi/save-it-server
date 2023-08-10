import pytest
from pytest_mock import MockerFixture
from services.authentication_service.common.enums.email_sign_up_status import EmailSignUpStatus
from common.objects.auto_mapper_config import AutoMapperConfig
from services.authentication_service.core.models.sign_up.sign_up_request import EmailSignUpRequest
from services.frontend_server.core.processor.frontend_server_processor import FrontendServerProcessor
from common.interface.auto_mapper_interface import AutoMapperInterface
from services.frontend_server.core.models.sign_up.frontend_server_sign_up_request import FrontendServerEmailSignUpRequest
from services.frontend_server.core.models.sign_up.frontend_server_sign_up_response import FrontendServerEmailSignUpResponse
from services.authentication_service.client.client_api.authentication_service_client import AuthenticationServiceClientInterface
from services.frontend_server.core.models.checklivestatus.frontend_check_live_status_response import FrontendServerCheckLiveStatusResponse
from common.enums.server_live_status import ServerLiveStatus
from services.authentication_service.client.api.sign_up.sign_up_request_api import EmailSignUpRequestApi
from services.authentication_service.client.api.sign_up.sign_up_response_api import EmailSignUpResponseApi
from services.authentication_service.client.api.checklivestatus.authentication_check_live_status_response_api import AuthenticationCheckLiveStatusResponseApi


class TestFrontendServerProcessor:
    @pytest.fixture(autouse=True)
    def setup_data(self, mocker: MockerFixture):
        self._mapper = mocker.MagicMock(AutoMapperInterface)
        self._authentication_service_client = mocker.MagicMock(AuthenticationServiceClientInterface)

        self._frontend_service_processor = FrontendServerProcessor(self._mapper, self._authentication_service_client)

    def test_checklivestatus_success(self):
        # Arrange
        self._authentication_service_client.checklivestatus.return_value = AuthenticationCheckLiveStatusResponseApi(status=ServerLiveStatus.ALIVE)

        # Act
        response = self._frontend_service_processor.checklivestatus()

        # Assert
        assert isinstance(response, FrontendServerCheckLiveStatusResponse)
        assert response.frontend_server_status == ServerLiveStatus.ALIVE
        assert response.authentication_service_status == ServerLiveStatus.ALIVE
        self._authentication_service_client.checklivestatus.assert_called_once()

    def test_checklivestatus_authentication_service_returns_dead(self):
        # Arrange
        self._authentication_service_client.checklivestatus.return_value = AuthenticationCheckLiveStatusResponseApi(status=ServerLiveStatus.DEAD)

        # Act
        response = self._frontend_service_processor.checklivestatus()

        # Assert
        assert isinstance(response, FrontendServerCheckLiveStatusResponse)
        assert response.frontend_server_status == ServerLiveStatus.ALIVE
        assert response.authentication_service_status == ServerLiveStatus.DEAD
        self._authentication_service_client.checklivestatus.assert_called_once()

    def test_checklivestatus_authentication_service_throw_exception(self, mocker: MockerFixture):
        # Arrange
        mock_method = mocker.patch.object(self._authentication_service_client, "checklivestatus")
        mock_method.side_effect = ValueError("404 Error page")

        # Act
        response = self._frontend_service_processor.checklivestatus()

        # Assert
        assert isinstance(response, FrontendServerCheckLiveStatusResponse)
        assert response.frontend_server_status == ServerLiveStatus.ALIVE
        assert response.authentication_service_status == ServerLiveStatus.DEAD
        self._authentication_service_client.checklivestatus.assert_called_once()

    def test_email_sign_up_success(self):
        # Arrange
        frontend_server_email_signup_request = FrontendServerEmailSignUpRequest('john@example.com', "qaqaqa")
        id_token = "id_token"

        class FrontendServerAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(EmailSignUpRequestApi, EmailSignUpRequest),
                    AutoMapperConfig(EmailSignUpResponseApi, FrontendServerEmailSignUpResponse),
                ]

        self._mapper = FrontendServerAutoMapper()
        self._authentication_service_client.email_sign_up.return_value = EmailSignUpResponseApi(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)
        self._frontend_service_processor = FrontendServerProcessor(self._mapper, self._authentication_service_client)

        # Act
        response = self._frontend_service_processor.email_sign_up(frontend_server_email_signup_request)

        # Assert
        assert isinstance(response, FrontendServerEmailSignUpResponse)
        assert response.is_success == True
        assert response.status == EmailSignUpStatus.SUCCESS
        assert response.id_token == id_token
        self._authentication_service_client.email_sign_up.assert_called_once()

    def test_email_sign_up_failure(self):
        # Arrange
        frontend_server_email_signup_request = FrontendServerEmailSignUpRequest('john@example.com', "qaqaqa")

        class FrontendServerAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(EmailSignUpRequestApi, EmailSignUpRequest),
                    AutoMapperConfig(EmailSignUpResponseApi, FrontendServerEmailSignUpResponse),
                ]

        self._mapper = FrontendServerAutoMapper()
        self._authentication_service_client.email_sign_up.return_value = EmailSignUpResponseApi(is_success=False, status=EmailSignUpStatus.EMAIL_EXISTS)
        self._frontend_service_processor = FrontendServerProcessor(self._mapper, self._authentication_service_client)

        # Act
        response = self._frontend_service_processor.email_sign_up(frontend_server_email_signup_request)

        # Assert
        assert isinstance(response, FrontendServerEmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.EMAIL_EXISTS
        assert response.id_token is None
        self._authentication_service_client.email_sign_up.assert_called_once()

    def test_email_login_success(self):
        # Arrange
        frontend_server_email_signup_request = FrontendServerEmailSignUpRequest('john@example.com', "qaqaqa")
        id_token = "id_token"

        class FrontendServerAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(EmailSignUpRequestApi, EmailSignUpRequest),
                    AutoMapperConfig(EmailSignUpResponseApi, FrontendServerEmailSignUpResponse),
                ]

        self._mapper = FrontendServerAutoMapper()
        self._authentication_service_client.email_login.return_value = EmailSignUpResponseApi(is_success=True, status=EmailSignUpStatus.SUCCESS, id_token=id_token)
        self._frontend_service_processor = FrontendServerProcessor(self._mapper, self._authentication_service_client)

        # Act
        response = self._frontend_service_processor.email_login(frontend_server_email_signup_request)

        # Assert
        assert isinstance(response, FrontendServerEmailSignUpResponse)
        assert response.is_success == True
        assert response.status == EmailSignUpStatus.SUCCESS
        assert response.id_token == id_token
        self._authentication_service_client.email_login.assert_called_once()

    def test_email_login_failure(self):
        # Arrange
        frontend_server_email_signup_request = FrontendServerEmailSignUpRequest('john@example.com', "qaqaqa")

        class FrontendServerAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(EmailSignUpRequestApi, EmailSignUpRequest),
                    AutoMapperConfig(EmailSignUpResponseApi, FrontendServerEmailSignUpResponse),
                ]

        self._mapper = FrontendServerAutoMapper()
        self._authentication_service_client.email_login.return_value = EmailSignUpResponseApi(is_success=False, status=EmailSignUpStatus.EMAIL_NOT_FOUND)
        self._frontend_service_processor = FrontendServerProcessor(self._mapper, self._authentication_service_client)

        # Act
        response = self._frontend_service_processor.email_login(frontend_server_email_signup_request)

        # Assert
        assert isinstance(response, FrontendServerEmailSignUpResponse)
        assert response.is_success == False
        assert response.status == EmailSignUpStatus.EMAIL_NOT_FOUND
        assert response.id_token is None
        self._authentication_service_client.email_login.assert_called_once()
