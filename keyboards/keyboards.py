"""Инлаин клавиатура, отображающаяся при команде /start"""

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon import LEXICON, WBLexicon


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Возвращает главную клавиатуру (команда /start)."""
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [
        KeyboardButton(text=description)
        for button, description in LEXICON.items()
        if not button.startswith("/") and button != WBLexicon.Subscribe
    ]

    kb_builder.row(*buttons, width=2)

    return kb_builder.as_markup()


def get_subscribe_keyboard(item_id: str) -> InlineKeyboardMarkup:
    """Клавиша подписки на оповещения."""
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    button = InlineKeyboardButton(
        text=LEXICON[WBLexicon.Subscribe],
        callback_data=item_id,
    )

    kb_builder.row(button)

    return kb_builder.as_markup()
