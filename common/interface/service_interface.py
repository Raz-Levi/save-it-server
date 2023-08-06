from abc import ABC, abstractmethod
from flask import Flask, scaffold
import json
from enum import Enum
from typing import Any
from flask import Response
from flask_restx import Api, Resource, Namespace


class ServiceInterface(ABC):
    def __init__(self):
        self._app = Flask(self.service_name)
        self._app.json_encoder = EnumEncoder
        self._api = Api(app=self._app, title=self.service_name, description=f'API for {self.service_name}', doc="/swagger")

        self._maintenance_namespace = self.define_namespace(namespace_name='maintenance', description='Maintenance Related Requests')
        self._api.add_namespace(self._maintenance_namespace)
        self.define_routes()

    @property
    @abstractmethod
    def service_name(self) -> str:
        pass

    def define_namespace(self, namespace_name: str, **kwargs) -> Namespace:
        return Namespace(name=f"{self.service_name}/{namespace_name}", **kwargs)

    def define_routes(self) -> None:
        @self._maintenance_namespace.route('/checklivestatus')
        class CheckLiveStatusResource(Resource):
            @staticmethod
            @self._api.doc()
            def post() -> bool:
                return self.checklivestatus()

    def checklivestatus(self) -> bool:
        return True

    def stringify_result(self, result: Any) -> Response:
        return Response(json.dumps(result.__dict__, cls=self._app.json_encoder), content_type='application/json')

    def run_service(self, port: int) -> None:
        self._app.run(debug=True, port=port)


class EnumEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.name
        return super().default(obj)
