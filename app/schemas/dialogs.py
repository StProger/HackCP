from pydantic import BaseModel

from datetime import datetime


class SDialogs(BaseModel):

    id: int
    user_id: int
    question: str
    answer: str
    feedback_user: str | None
    rating: int | None
    comment: str | None
    created_at: datetime
