from abc import ABC, abstractmethod
import json
from enum import Enum
from typing import Any
from flask import Flask, Response
from flask_restx import Api, Namespace
from flask_cors import CORS


class ServiceInterface(ABC):
    def __init__(self):
        self._app = Flask(self.service_name)
        CORS(self._app)
        self._app.json_encoder = EnumEncoder
        self._api = Api(app=self._app, title=self.service_name, description=f'API for {self.service_name}', doc="/swagger", version="", )

        self._maintenance_namespace = self.define_namespace(namespace_name='maintenance', description='Maintenance Related Requests')
        self._api.add_namespace(self._maintenance_namespace)
        self.define_routes()

    @property
    @abstractmethod
    def service_name(self) -> str:
        pass

    @abstractmethod
    def define_routes(self) -> None:
        pass

    def define_namespace(self, namespace_name: str, **kwargs) -> Namespace:
        return Namespace(name=f"{self.service_name}/{namespace_name}", **kwargs)

    def stringify_result(self, result: Any) -> Response:
        return Response(json.dumps(result.__dict__, cls=self._app.json_encoder), content_type='application/json')

    def run_service(self, configuration: object) -> None:
        self._app.config.from_object(configuration)
        self._app.run()


class EnumEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.name
        return super().default(obj)
