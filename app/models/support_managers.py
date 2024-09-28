from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TEXT, BIGINT

from app.db import Base


class Managers(Base):

    __tablename__ = 'support_managers'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BIGINT, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(TEXT, nullable=False)
    fio_manager: Mapped[str] = mapped_column(TEXT, nullable=False)
    username: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
