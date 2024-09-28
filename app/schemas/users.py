from pydantic import BaseModel

from datetime import datetime


class SUser(BaseModel):

    id: int
    business_id: str | None
    username: str | None
    first_name: str | None
    last_name: str | None
    need_manager: bool
    model_name: str
    created_at: datetime
