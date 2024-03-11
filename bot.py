"""Telegram MyTestWBBot"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from database import create_tables

from config import settings
from handlers.main_handlers import router as main_router
from handlers.other_handlers import router as other_router


dispatcher: Dispatcher = Dispatcher()

async def main():
    # Логгирование
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    # Создание таблиц, если БД пустая
    await create_tables()

    bot: Bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )


    await bot.delete_webhook(drop_pending_updates=True)

    dispatcher.include_router(main_router)
    dispatcher.include_router(other_router)

    await dispatcher.start_polling(bot)
    dispatcher.run_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
