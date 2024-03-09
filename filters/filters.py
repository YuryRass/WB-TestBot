"""Фильтры, накладывающиеся на роутеры"""

from aiogram.filters import BaseFilter
from aiogram.types import Message

from lexicon import WBLexicon, LEXICON


class IsGetProductInfo(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text == LEXICON[WBLexicon.GetInfo]