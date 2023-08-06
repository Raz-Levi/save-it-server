import pytest
from dataclasses import dataclass
from common.interface.auto_mapper_interface import AutoMapperInterface
from common.objects.auto_mapper_config import AutoMapperConfig


class TestAutoMapperInterface:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self._auto_mapper = None

    def test_map_same_attributes(self):
        # Arrange
        first_name = 'John'
        last_name = 'Doe'
        age = 30
        email = 'john@example.com'

        @dataclass
        class SourceObject:
            first_name: str
            last_name: str
            age: int
            email: str

        @dataclass
        class DestinationObject:
            first_name: str
            last_name: str
            age: int
            email: str

        class AutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self) -> list:
                return [AutoMapperConfig(SourceObject, DestinationObject)]

        self._auto_mapper = AutoMapper()

        # Act
        source_object = SourceObject(first_name=first_name, last_name=last_name, age=age, email=email)
        destination_object = self._auto_mapper(source_object, DestinationObject)

        # Assert
        assert type(destination_object) == DestinationObject
        assert destination_object.first_name == first_name
        assert destination_object.last_name == last_name
        assert destination_object.age == age
        assert destination_object.email == email

    def test_map_complex_objects(self):
        # Arrange
        first_name = 'John'
        last_name = 'Doe'
        age = 30
        email = 'john@example.com'

        @dataclass
        class SourceObject:
            first_name: str
            last_name: str
            age: int
            email: str

        @dataclass
        class DestinationObject:
            full_name: str
            age: int
            email: str

        config = {
            'full_name': lambda source_obj: f"{source_obj.first_name} {source_obj.last_name}",
        }

        class AutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self) -> list:
                return [AutoMapperConfig(SourceObject, DestinationObject, config)]

        self._auto_mapper = AutoMapper()

        # Act
        source_object = SourceObject(first_name=first_name, last_name=last_name, age=age, email=email)
        destination_object = self._auto_mapper(source_object, DestinationObject)

        # Assert
        assert type(destination_object) == DestinationObject
        assert destination_object.full_name == f"{first_name} {last_name}"
        assert destination_object.age == age
        assert destination_object.email == email

    def test_map_opposite(self):
        # Arrange
        first_name = 'John'
        last_name = 'Doe'
        age = 30
        email = 'john@example.com'

        @dataclass
        class SourceObject:
            first_name: str
            last_name: str
            age: int
            email: str

        @dataclass
        class DestinationObject:
            first_name: str
            last_name: str
            age: int
            email: str

        config = {
            'first_name': 'last_name',
            'last_name': 'first_name',
        }

        class AutoMapper(AutoMapperInterface):
            @property
            def mapping_config(self) -> list:
                return [AutoMapperConfig(SourceObject, DestinationObject, config)]

        self._auto_mapper = AutoMapper()

        # Act
        source_object = SourceObject(first_name=first_name, last_name=last_name, age=age, email=email)
        destination_object = self._auto_mapper(source_object, DestinationObject)

        # Assert
        assert type(destination_object) == DestinationObject
        assert destination_object.first_name == last_name
        assert destination_object.last_name == first_name
        assert destination_object.age == age
        assert destination_object.email == email
