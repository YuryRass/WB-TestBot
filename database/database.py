"""Модуль для создания ассинхронного подключения к БД"""

from typing_extensions import Annotated
from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from config import settings

bigint = Annotated[int, "bigint"]


engine: AsyncEngine = create_async_engine(settings.DATABASE_URL)

async_session = async_sessionmaker(bind=engine, expire_on_commit=True)


class Base(DeclarativeBase):
    type_annotation_map = {bigint: BigInteger()}

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


async def create_tables() -> None:
    """Создание таблиц БД"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
