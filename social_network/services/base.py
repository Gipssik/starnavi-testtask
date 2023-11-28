from typing import TypeVar, Generic, Sequence, Type

from sqlalchemy import select, update, exists, delete, insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from social_network.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, filters: Sequence, options: Sequence = ()) -> ModelType | None:
        """Get one obj from database"""
        query = select(self.model).filter(*filters).options(*options).limit(1)
        return await self.session.scalar(query)

    async def get_all(self, query: Query) -> list[ModelType]:
        """Get filtered objs from database"""
        return (await self.session.scalars(query)).all()  # type: ignore

    async def update(self, filters: Sequence, values: dict) -> None:
        """Update instance in DB"""
        query = update(self.model).where(*filters).values(**values).execution_options(synchronize_session="fetch")
        await self.session.execute(query)

    async def insert(self, values: dict) -> None:
        """Insert new obj to DB"""
        query = insert(self.model).values(**values).execution_options(synchronize_session="fetch")
        await self.session.execute(query)
        await self.session.commit()

    async def insert_obj(self, obj: Base) -> ModelType:
        """Insert new obj to DB"""
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def delete(self, filters: Sequence) -> None:
        """Delete obj from DB"""
        query = delete(self.model).where(*filters)
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, filters: Sequence) -> bool:
        """Check if obj record exists in DB"""
        query = exists(self.model).where(*filters).select()
        return await self.session.scalar(query)

    async def count(self, filters: Sequence) -> int:
        """Count obj records in DB"""
        query = select(func.count()).where(*filters)
        return await self.session.scalar(query)
