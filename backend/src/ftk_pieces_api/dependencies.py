from typing import Annotated, TypeVar

from fastapi import Depends, HTTPException, status, Path
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession

from .database import session_factory, Student, Base


async def get_db():
    try:
        session = session_factory()
        yield session
        await session.commit()
    finally:
        await session.close()  # type: ignore


DB = Annotated[AsyncSession, Depends(get_db)]


class _ModelDependency:
    @staticmethod
    def build_dependency(db_model: type[Base], name: str):
        async def generated(item_id: Annotated[int, Path(alias=name + "_id")], db: DB):
            item = (
                await db.execute(sql.select(db_model).where(db_model.id == item_id))
            ).scalar()
            if item is None:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND, f"{name} with such id does not exists"
                )
            return item

        return generated

    Student = Annotated[Student, Depends(build_dependency(Student, "student"))]


model = _ModelDependency


class _ExistsDependency:
    @staticmethod
    def build_dependency(db_model: type[Base], name: str):
        async def generated(item_id: Annotated[int, Path(alias=name + "_id")], db: DB):
            item = (
                await db.execute(sql.select(db_model.id).where(db_model.id == item_id))
            ).scalar()
            if item is None:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND, f"{name} with such id does not exists"
                )
            return item

        return generated

    Student = Annotated[int, Depends(build_dependency(Student, "student"))]


exists = _ExistsDependency
