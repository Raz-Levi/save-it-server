import threading
from common.configuration.server_configutrations.server_configurations_local import ServerConfigurationsLocal
from services.frontend_server.common.frontend_server_injector import FrontendServerInjector
from services.frontend_server.core.service.frontend_server_service import FrontendServer
from services.authentication_service.common.authentication_service_injector import AuthenticationServiceInjector
from services.authentication_service.core.service.authentication_service import AuthenticationService


def run_server():
    server_config = ServerConfigurationsLocal()  # TODO- update tp QA and Prod

    frontend_server = threading.Thread(target=lambda: FrontendServerInjector.inject(FrontendServer).run_service(server_config.frontend_server_config.port))
    authentication_service = threading.Thread(target=lambda: AuthenticationServiceInjector.inject(AuthenticationService).run_service(server_config.authentication_service_config.port))

    frontend_server.start()
    authentication_service.start()


if __name__ == '__main__':
    run_server()
