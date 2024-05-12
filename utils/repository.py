from abc import ABC, abstractmethod

from fastapi_cache.decorator import cache
from sqlalchemy import insert, select

from db.db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all():
        pass


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def get_all(self, filters: dict | None = None):
        async with async_session_maker() as session:
            query = select(self.model)

            if filters:
                query = query.filter_by(**filters)

            result = await session.execute(query)
            return result.scalars().all()

    async def get_one(self, filters: dict | None = None):
        async with async_session_maker() as session:
            query = select(self.model)

            if filters:
                query = query.filter_by(**filters)

            result = await session.execute(query)
            return result.scalar()

    async def insert_data(self, params: dict):
        async with async_session_maker() as session:
            query = insert(self.model).values(**params)
            await session.execute(query)
            await session.commit()
