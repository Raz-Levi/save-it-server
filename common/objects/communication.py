import requests
from typing import Callable
from common.interface.communication_interface import CommunicationInterface


class Communication(CommunicationInterface):
    def get(self) -> Callable:
        return requests.get

    def post(self) -> Callable:
        return requests.post

    def patch(self) -> Callable:
        return requests.patch
