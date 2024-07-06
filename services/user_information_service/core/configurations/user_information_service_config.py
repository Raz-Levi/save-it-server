from hidden_files import app_key_api
from abc import ABC, abstractmethod


class UserInformationConfigurationsInterface(ABC):
    @abstractmethod
    def user_information_database_url(self, collection_name: str, document_id: str) -> str:
        pass


class UserInformationConfigurations(UserInformationConfigurationsInterface):
    _APP_KEY_API = app_key_api.APP_KEY_API

    def user_information_database_url(self, collection_name: str, document_id: str) -> str:
        return f'https://firestore.googleapis.com/v1/projects/save-it-244b7/databases/(default)/documents/{collection_name}/{document_id}?key={self._APP_KEY_API}'
