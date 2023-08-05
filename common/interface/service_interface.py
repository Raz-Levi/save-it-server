from abc import ABC, abstractmethod
from flask import Flask
import json
from enum import Enum
from typing import Any
from flask import Response


class ServiceInterface(ABC):
    def __init__(self):
        self.app = Flask(self.get_service_name)
        self.app.json_encoder = EnumEncoder
        self.define_routes()

    @property
    @abstractmethod
    def get_service_name(self) -> str:
        pass

    def define_routes(self) -> None:
        @self.app.route(f"/{self.get_service_name}/checklivestatus")
        def email_sign_up() -> str:
            return self.get_service_name + " live"

    def stringify_result(self, result: Any) -> Response:
        return Response(json.dumps(result.__dict__, cls=self.app.json_encoder), content_type='application/json')

    def run_service(self, port: int) -> None:
        self.app.run(debug=True, port=port)


class EnumEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)
