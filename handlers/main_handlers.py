from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state

from lexicon import LEXICON
from keyboards import get_main_keyboard


router: Router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def command_start(message: Message):
    # главная клавиатура для пользователя
    main_keyboard = get_main_keyboard()
    await message.answer(
        text=f"<b>Рад Вас видеть, {message.from_user.full_name}!</b>\n\n"
        + LEXICON["/start"],
        reply_markup=main_keyboard,
    )


@router.message(Command(commands="help"), StateFilter(default_state))
async def command_help(message: Message):
    await message.answer(text=LEXICON["/help"])
