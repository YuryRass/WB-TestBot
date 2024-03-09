"""Create Read Update Delete"""

from datetime import datetime
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from database.model import WBHistory
from database import async_session


class WBCrud:
    """Базовый класс основных операций для БД Продукты."""

    model = WBHistory

    @classmethod
    async def get_last_five_records(cls, user_tg_id: int):
        """Возвращает последние пять записей модели."""
        query = select(cls.model).where(cls.model.user_tg_id == user_tg_id).order_by(cls.model.id.desc()).limit(5)
        async with async_session() as session:
            res = await session.execute(query)
            return res.scalars().all()

    @classmethod
    async def add(cls, **data) -> None:
        """Добавление записи в модель."""
        stmt = insert(cls.model).values(**data)
        session: AsyncSession
        async with async_session() as session:
            await session.execute(stmt)
            await session.commit()
