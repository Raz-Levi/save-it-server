import requests
from common.interface.communication_interface import CommunicationInterface


class Communication(CommunicationInterface):
    def __init__(self):
        super().__init__(requests.post)
