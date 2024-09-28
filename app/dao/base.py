from sqlalchemy import Result, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session_maker


class BaseDAO:

    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):

        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result: Result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):

        async with async_session_maker() as session:
            session: AsyncSession
            query = select(cls.model).filter_by(**filter_by)
            result: Result = await session.execute(query)
            return result.one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)

            return result.mappings().all()

    @classmethod
    async def add(cls, **data):

        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result: Result = await session.execute(query)
            await session.commit()
            return result.scalar()