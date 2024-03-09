"""Фильтры, накладывающиеся на роутеры"""

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from lexicon import WBLexicon, LEXICON


class IsGetProductInfo(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text == LEXICON[WBLexicon.GetInfo]

class IsGetWBHistory(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text == LEXICON[WBLexicon.GetWBHistory]

class IsSubscribeCallback(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()

class IsCancelSubscription(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text == LEXICON[WBLexicon.StopNotifications]