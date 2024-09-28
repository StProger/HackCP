from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TEXT, DateTime, BIGINT, ForeignKey, INTEGER

from datetime import datetime

import pytz

from app.db import Base


class Dialogs(Base):

    __tablename__ = 'dialogs'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'), nullable=False)
    question: Mapped[str] = mapped_column(TEXT, nullable=False)
    answer: Mapped[str] = mapped_column(TEXT, nullable=False)
    feedback_user: Mapped[str] = mapped_column(TEXT, nullable=True)
    rating: Mapped[int] = mapped_column(INTEGER, nullable=True)
    comment: Mapped[str] = mapped_column(TEXT, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), default=datetime.now(pytz.timezone("Europe/Moscow")))