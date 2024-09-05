import re
import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import orm


engine = create_async_engine(
    os.getenv("POSTGRES_CONNECTION_STRING"), echo=True
)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


WORD_PATTERN = re.compile("[a-zA-Z][^A-Z]*")


def parse_tablename(name: str) -> str:
    match = re.findall(WORD_PATTERN, name)
    if match[-1][-1] == "y":
        match[-1] = match[-1][:-1] + "ies"
    else:
        match[-1] += "s"
    return "_".join(m.lower() for m in match)


class Base(orm.DeclarativeBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    @orm.declared_attr.directive
    def __tablename__(cls) -> str:
        return parse_tablename(cls.__name__)
