from hidden_files import authentication


class DatabaseConfigurations:
    @staticmethod
    def get_service_account_key_path() -> str:
        return "hidden_files/serviceAccountKey.json"

    @staticmethod
    def get_app_key_api() -> str:
        return app_key_api.APP_KEY_API
