import requests
from typing import Callable
from common.interface.communication_interface import CommunicationInterface


class Communication(CommunicationInterface):
    def post(self) -> Callable:
        return requests.post
