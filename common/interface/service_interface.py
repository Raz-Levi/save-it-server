from abc import ABC, abstractmethod
from flask import Flask, scaffold
import json
from enum import Enum
from typing import Any
from flask import Response


class ServiceInterface(ABC):
    def __init__(self):
        self.app = Flask(self.service_name)
        self.app.json_encoder = EnumEncoder
        self.define_routes()

    def define_route(self, route_name: str, **kwargs) -> scaffold.T_route:
        return self.app.route(rule=f"/{self.service_name}/{route_name}", **kwargs)

    @property
    @abstractmethod
    def service_name(self) -> str:
        pass

    def define_routes(self) -> None:
        self.define_route("/checklivestatus")(lambda: self.checklivestatus())

    def checklivestatus(self) -> str:
        return self.service_name + " live"

    def stringify_result(self, result: Any) -> Response:
        return Response(json.dumps(result.__dict__, cls=self.app.json_encoder), content_type='application/json')

    def run_service(self, port: int) -> None:
        self.app.run(debug=True, port=port)


class EnumEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)
