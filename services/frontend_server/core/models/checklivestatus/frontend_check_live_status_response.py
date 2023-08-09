from dataclasses import dataclass
from common.enums.server_live_status import ServerLiveStatus


@dataclass
class FrontendServerCheckLiveStatusResponse:
    frontend_server_status: ServerLiveStatus
    authentication_service_status: ServerLiveStatus = ServerLiveStatus.DEAD
