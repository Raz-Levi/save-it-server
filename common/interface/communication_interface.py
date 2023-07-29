from typing import Callable


class CommunicationInterface:
    def __init__(self, post: Callable):
        self.post = post
