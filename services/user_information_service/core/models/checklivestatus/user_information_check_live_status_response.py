from dataclasses import dataclass
from common.enums.server_live_status import ServerLiveStatus


@dataclass
class UserInformationCheckLiveStatusResponse:
    status: ServerLiveStatus
