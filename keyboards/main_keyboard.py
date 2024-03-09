"""Инлаин клавиатура, отображающаяся при команде /start"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon import LEXICON


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Возвращает главную клавиатуру (команда /start)."""
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = [
        KeyboardButton(text=description, callback_data=button)
        for button, description in LEXICON.items()
        if not button.startswith("/")
    ]

    kb_builder.row(*buttons, width=3)

    return kb_builder.as_markup()
