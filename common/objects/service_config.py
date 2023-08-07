class ServiceConfig:
    def __init__(self, url: str, port: int):
        self.url = url
        self.port = port

    @property
    def full_server_url(self) -> str:
        return f'{self.url}:{str(self.port)}'
