import pytest
from pytest_mock import MockerFixture
from common.objects.logger import Logger
from common.enums.server_live_status import ServerLiveStatus
from common.interface.auto_mapper_interface import AutoMapperInterface
from common.objects.auto_mapper_config import AutoMapperConfig
from services.user_information_service.common.enums.get_user_information_status import GetUserInformationStatus
from services.user_information_service.common.enums.set_user_information_status import SetUserInformationStatus
from services.user_information_service.core.models.checklivestatus.user_information_check_live_status_response import UserInformationCheckLiveStatusResponse
from services.user_information_service.core.models.dal.user_information.dal_get_user_information_response import DalGetUserInformationResponse
from services.user_information_service.core.models.dal.user_information.dal_set_user_information_response import DalSetUserInformationDalResponse
from services.user_information_service.core.models.dal.user_information.dal_user_information import DalUserInformation
from services.user_information_service.core.models.get_user_information.get_user_information_request import GetUserInformationRequest
from services.user_information_service.core.models.get_user_information.get_user_information_response import GetUserInformationResponse
from services.user_information_service.core.models.set_user_information.set_user_information_request import SetUserInformationRequest
from services.user_information_service.core.models.set_user_information.set_user_information_response import SetUserInformationResponse
from services.user_information_service.core.processor.user_information_service_processor import UserInformationServiceProcessor
from services.user_information_service.core.repositories.user_information_repository import UserInformationRepositoryInterface


class TestUserInformationServiceProcessor:
    @pytest.fixture(autouse=True)
    def setup_data(self, mocker: MockerFixture):
        self._mapper = mocker.MagicMock(AutoMapperInterface)
        self._user_information_repository = mocker.MagicMock(UserInformationRepositoryInterface)
        
        # TODO- mock logger and add tests for it
        self._user_information_service_processor = UserInformationServiceProcessor(self._mapper, Logger(), self._user_information_repository)

    def test_checklivestatus_success(self):
        # Act
        response = self._user_information_service_processor.checklivestatus()

        # Assert
        assert type(response) == UserInformationCheckLiveStatusResponse
        assert response.status == ServerLiveStatus.ALIVE

    def test_set_user_information_success(self):
        # Arrange
        set_user_information_request = SetUserInformationRequest(user_id='123', email='john@gmail.com', full_name="John Doe", phone="0549999999")
        self._user_information_repository.set_user_information_by_user_id.return_value = DalSetUserInformationDalResponse(is_success=True, status=SetUserInformationStatus.SUCCESS)

        class UserInformationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalSetUserInformationDalResponse, SetUserInformationResponse),
                ]

        self._mapper = UserInformationServiceAutoMapper()
        self._user_information_service_processor = UserInformationServiceProcessor(self._mapper, Logger(), self._user_information_repository)

        # Act
        response = self._user_information_service_processor.set_user_information(set_user_information_request)

        # Assert
        assert isinstance(response, SetUserInformationResponse)
        assert response.is_success is True
        assert response.status == SetUserInformationStatus.SUCCESS
        self._user_information_repository.set_user_information_by_user_id.assert_called_once()

    def test_set_user_information_repository_failed(self):
        # Arrange
        set_user_information_request = SetUserInformationRequest(user_id='123', email='john@gmail.com', full_name="John Doe", phone="0549999999")
        self._user_information_repository.set_user_information_by_user_id.return_value = DalSetUserInformationDalResponse(is_success=False, status=SetUserInformationStatus.UNKNOWN_ERROR)

        class UserInformationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalSetUserInformationDalResponse, SetUserInformationResponse),
                ]

        self._mapper = UserInformationServiceAutoMapper()
        self._user_information_service_processor = UserInformationServiceProcessor(self._mapper, Logger(), self._user_information_repository)

        # Act
        response = self._user_information_service_processor.set_user_information(set_user_information_request)

        # Assert
        assert isinstance(response, SetUserInformationResponse)
        assert response.is_success is False
        assert response.status == SetUserInformationStatus.UNKNOWN_ERROR
        self._user_information_repository.set_user_information_by_user_id.assert_called_once()

    def test_set_user_information_invalid_phone(self):
        # Arrange
        set_user_information_request = SetUserInformationRequest(user_id='123', email='john@gmail.com', full_name="John Doe", phone="123")
        self._user_information_repository.set_user_information_by_user_id.return_value = DalSetUserInformationDalResponse(is_success=True, status=SetUserInformationStatus.SUCCESS)

        class UserInformationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalSetUserInformationDalResponse, SetUserInformationResponse),
                ]

        self._mapper = UserInformationServiceAutoMapper()
        self._user_information_service_processor = UserInformationServiceProcessor(self._mapper, Logger(), self._user_information_repository)

        # Act
        response = self._user_information_service_processor.set_user_information(set_user_information_request)

        # Assert
        assert isinstance(response, SetUserInformationResponse)
        assert response.is_success is False
        assert response.status == SetUserInformationStatus.INVALID_PHONE
        self._user_information_repository.set_user_information_by_user_id.assert_not_called()

    def test_set_user_information_invalid_email(self):
        # Arrange
        set_user_information_request = SetUserInformationRequest(user_id='123', email='john@gmail', full_name="John Doe", phone="0549999999")
        self._user_information_repository.set_user_information_by_user_id.return_value = DalSetUserInformationDalResponse(is_success=True, status=SetUserInformationStatus.SUCCESS)

        class UserInformationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalSetUserInformationDalResponse, SetUserInformationResponse),
                ]

        self._mapper = UserInformationServiceAutoMapper()
        self._user_information_service_processor = UserInformationServiceProcessor(self._mapper, Logger(), self._user_information_repository)

        # Act
        response = self._user_information_service_processor.set_user_information(set_user_information_request)

        # Assert
        assert isinstance(response, SetUserInformationResponse)
        assert response.is_success is False
        assert response.status == SetUserInformationStatus.INVALID_EMAIL
        self._user_information_repository.set_user_information_by_user_id.assert_not_called()

    def test_set_user_information_empty_name(self):
        # Arrange
        set_user_information_request = SetUserInformationRequest(user_id='123', email='john@gmail.com', full_name="", phone="0549999999")
        self._user_information_repository.set_user_information_by_user_id.return_value = DalSetUserInformationDalResponse(is_success=True, status=SetUserInformationStatus.SUCCESS)

        class UserInformationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalSetUserInformationDalResponse, SetUserInformationResponse),
                ]

        self._mapper = UserInformationServiceAutoMapper()
        self._user_information_service_processor = UserInformationServiceProcessor(self._mapper, Logger(), self._user_information_repository)

        # Act
        response = self._user_information_service_processor.set_user_information(set_user_information_request)

        # Assert
        assert isinstance(response, SetUserInformationResponse)
        assert response.is_success is False
        assert response.status == SetUserInformationStatus.INVALID_NAME
        self._user_information_repository.set_user_information_by_user_id.assert_not_called()

    def test_set_user_information_space_in_end_of_name(self):
        # Arrange
        set_user_information_request = SetUserInformationRequest(user_id='123', email='john@gmail.com', full_name="John Doe ", phone="0549999999")
        self._user_information_repository.set_user_information_by_user_id.return_value = DalSetUserInformationDalResponse(is_success=True, status=SetUserInformationStatus.SUCCESS)

        class UserInformationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalSetUserInformationDalResponse, SetUserInformationResponse),
                ]

        self._mapper = UserInformationServiceAutoMapper()
        self._user_information_service_processor = UserInformationServiceProcessor(self._mapper, Logger(), self._user_information_repository)

        # Act
        response = self._user_information_service_processor.set_user_information(set_user_information_request)

        # Assert
        assert isinstance(response, SetUserInformationResponse)
        assert response.is_success is False
        assert response.status == SetUserInformationStatus.INVALID_NAME
        self._user_information_repository.set_user_information_by_user_id.assert_not_called()

    def test_set_user_information_space_in_start_of_name(self):
        # Arrange
        set_user_information_request = SetUserInformationRequest(user_id='123', email='john@gmail.com', full_name=" John Doe", phone="0549999999")
        self._user_information_repository.set_user_information_by_user_id.return_value = DalSetUserInformationDalResponse(is_success=True, status=SetUserInformationStatus.SUCCESS)

        class UserInformationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalSetUserInformationDalResponse, SetUserInformationResponse),
                ]

        self._mapper = UserInformationServiceAutoMapper()
        self._user_information_service_processor = UserInformationServiceProcessor(self._mapper, Logger(), self._user_information_repository)

        # Act
        response = self._user_information_service_processor.set_user_information(set_user_information_request)

        # Assert
        assert isinstance(response, SetUserInformationResponse)
        assert response.is_success is False
        assert response.status == SetUserInformationStatus.INVALID_NAME
        self._user_information_repository.set_user_information_by_user_id.assert_not_called()

    def test_set_user_information_non_alphabetic_name(self):
        # Arrange
        set_user_information_request = SetUserInformationRequest(user_id='123', email='john@gmail.com', full_name="John_Doe", phone="0549999999")
        self._user_information_repository.set_user_information_by_user_id.return_value = DalSetUserInformationDalResponse(is_success=True, status=SetUserInformationStatus.SUCCESS)

        class UserInformationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalSetUserInformationDalResponse, SetUserInformationResponse),
                ]

        self._mapper = UserInformationServiceAutoMapper()
        self._user_information_service_processor = UserInformationServiceProcessor(self._mapper, Logger(), self._user_information_repository)

        # Act
        response = self._user_information_service_processor.set_user_information(set_user_information_request)

        # Assert
        assert isinstance(response, SetUserInformationResponse)
        assert response.is_success is False
        assert response.status == SetUserInformationStatus.INVALID_NAME
        self._user_information_repository.set_user_information_by_user_id.assert_not_called()

    def test_get_user_information_success(self):
        # Arrange
        user_id = '123'
        email = 'john@gmail.com'
        full_name = "John Doe"
        phone = "0549999999"

        get_user_information_request = GetUserInformationRequest(user_id=user_id)
        user_information = DalUserInformation(user_id=user_id, email=email, full_name=full_name, phone=phone)

        self._user_information_repository.get_user_information_by_user_id.return_value = DalGetUserInformationResponse(is_success=True, dal_user_information=user_information, status=GetUserInformationStatus.SUCCESS)

        class UserInformationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalGetUserInformationResponse, GetUserInformationResponse),
                ]

        self._mapper = UserInformationServiceAutoMapper()
        self._user_information_service_processor = UserInformationServiceProcessor(self._mapper, Logger(), self._user_information_repository)

        # Act
        response = self._user_information_service_processor.get_user_information(get_user_information_request)

        # Assert
        assert isinstance(response, GetUserInformationResponse)
        assert response.is_success is True
        assert response.user_id == user_id
        assert response.email == email
        assert response.full_name == full_name
        assert response.phone == phone
        assert response.status == GetUserInformationStatus.SUCCESS
        self._user_information_repository.get_user_information_by_user_id.assert_called_once()

    def test_get_user_information_failure(self):
        # Arrange
        user_id = '123'
        get_user_information_request = GetUserInformationRequest(user_id=user_id)
        self._user_information_repository.get_user_information_by_user_id.return_value = DalGetUserInformationResponse(is_success=False, dal_user_information=None, status=GetUserInformationStatus.UNKNOWN_ERROR)

        class UserInformationServiceAutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self):
                return [
                    AutoMapperConfig(DalGetUserInformationResponse, GetUserInformationResponse),
                ]

        self._mapper = UserInformationServiceAutoMapper()
        self._user_information_service_processor = UserInformationServiceProcessor(self._mapper, Logger(), self._user_information_repository)

        # Act
        response = self._user_information_service_processor.get_user_information(get_user_information_request)

        # Assert
        assert isinstance(response, GetUserInformationResponse)
        assert response.is_success is False
        assert response.user_id is None
        assert response.email is None
        assert response.full_name is None
        assert response.phone is None
        assert response.status == GetUserInformationStatus.UNKNOWN_ERROR
        self._user_information_repository.get_user_information_by_user_id.assert_called_once()