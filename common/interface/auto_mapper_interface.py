from marshmallow_dataclass import dataclass
from typing import Any
from common.objects.auto_mapper_config import AutoMapperConfig


class AutoMapperInterface:
    def __init__(self):
        self.mapping_config = []  # Abstract

    def __call__(self, source_object: Any, destination_class: Any, mapping_config: dict = None) -> Any:
        if mapping_config is None:
            mapping_config = self.find_auto_mapper_config_by_name(type(source_object), destination_class)

        schema = dataclass(destination_class)
        mapped_data = {}

        for destination_attribute_name, mapping_value in mapping_config.items():
            if callable(mapping_value):
                mapped_data[destination_attribute_name] = mapping_value(source_object)

            elif isinstance(mapping_value, str):
                mapped_data[destination_attribute_name] = getattr(source_object, mapping_value)

        source_attributes = [attr for attr in dir(source_object) if not attr.startswith("__")]
        destination_attributes = [attr for attr in destination_class.__init__.__code__.co_varnames if attr != "self"]
        common_attributes = [common_attribute for common_attribute in source_attributes if common_attribute in destination_attributes and not common_attribute in mapping_config.keys()]

        for destination_attribute_name in common_attributes:
            mapped_data[destination_attribute_name] = getattr(source_object, destination_attribute_name)

        return schema.Schema().load(mapped_data)

    def find_auto_mapper_config_by_name(self, source_class: Any, destination_class: Any) -> dict:
        auto_mapper_config_name = AutoMapperConfig.get_map_name(source_class, destination_class)
        config = {}

        for auto_mapper in self.mapping_config:
            if auto_mapper.name == auto_mapper_config_name:
                config = auto_mapper.config

        return config
