"""Описание таблиц БД"""

from datetime import datetime

from sqlalchemy.orm import Mapped

from database import Base, bigint


class WBHistory(Base):
    """Товары с WB."""

    user_tg_id: Mapped[bigint]
    date_time: Mapped[datetime]
    item_number: Mapped[int]

    def __str__(self) -> str:
        return f'<b><em>Артикул</em></b>={self.item_number} - <b>{self.date_time.strftime("%d.%m.%y %H:%M:%S")}</b>'
