from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TEXT, BOOLEAN, DateTime, BIGINT

from datetime import datetime

import pytz

from app.db import Base


class Users(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    business_id: Mapped[str] = mapped_column(TEXT, nullable=True)
    username: Mapped[str] = mapped_column(TEXT, nullable=True)
    first_name: Mapped[str] = mapped_column(TEXT, nullable=True)
    last_name: Mapped[str] = mapped_column(TEXT, nullable=True)
    need_manager: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    model_name: Mapped[str] = mapped_column(TEXT, default="sbert")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), default=datetime.now(pytz.timezone("Europe/Moscow")))