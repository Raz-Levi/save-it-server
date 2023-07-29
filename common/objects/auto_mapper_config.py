from typing import Any


class AutoMapperConfig:
    def __init__(self, source_class: Any, destination_class: Any, config: dict = {}):
        self.name = self.get_map_name(source_class, destination_class)
        self.config = config

    @staticmethod
    def get_map_name(source_class: Any, destination_class: Any) -> Any:
        return f'{source_class.__name__}_{destination_class.__name__}'
