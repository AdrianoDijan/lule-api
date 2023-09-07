from pydantic import BaseModel

from ...constants import ActionStatus


class StatusResponse(BaseModel):
    status: ActionStatus
