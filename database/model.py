"""Описание таблиц БД"""

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from database import Base, bigint


class Product(Base):
    """Товары с WB"""
    user_tg_id: Mapped[bigint] = mapped_column(unique=True)
    date_time: Mapped[datetime]
    item_number: Mapped[int]