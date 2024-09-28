from sqlalchemy import update, select, and_, Result

from app.models.dialogs import Dialogs
from app.dao.base import BaseDAO

from app.db import async_session_maker


class DialogsDAO(BaseDAO):
    model = Dialogs

    @classmethod
    async def update(cls, id_model, **data):

        async with async_session_maker() as session:

            stmt = (
                update(
                    Dialogs
                )
                .where(Dialogs.id == id_model)
                .values(**data)
            )

            await session.execute(stmt)
            await session.commit()


    @classmethod
    async def get_dialog(cls, user_id):

        async with async_session_maker() as session:

            stmt = (
                select(
                    Dialogs
                )
                .where(
                    and_(
                        Dialogs.user_id == user_id,
                        Dialogs.rating == None,
                        Dialogs.comment == None
                    )
                )
                .order_by(Dialogs.created_at.desc())
                .limit(1)
            )

            result: Result = await session.execute(stmt)

            return result.scalar_one_or_none()