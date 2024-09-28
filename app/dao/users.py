from sqlalchemy import update

from app.models.users import Users
from app.dao.base import BaseDAO
from app.db import async_session_maker


class UsersDAO(BaseDAO):

    model = Users

    @classmethod
    async def update(cls, id_model: int, **data):

        async with async_session_maker() as session:

            stmt = (
                update(
                    Users
                )
                .where(Users.id == id_model)
                .values(**data)
            )

            await session.execute(stmt)
            await session.commit()