import asyncio
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
from filters import (
    IsGetProductInfo,
    IsGetWBHistory,
    IsSubscribeCallback,
    IsCancelSubscription,
)
from api_requests import WBProduct
from keyboards import get_subscribe_keyboard
from database.crud import WBCrud

from config import settings


class WBStates(StatesGroup):
    get_info = State()
    start_loop = State()


router: Router = Router()


@router.message(IsGetProductInfo())
async def input_product_item(message: Message, state: FSMContext):
    await state.set_state(state=WBStates.get_info)
    await message.answer(text="Введите артикул товара")


@router.message(IsGetWBHistory())
async def get_wb_info_from_db(message: Message):
    history = await WBCrud.get_last_five_records(int(message.from_user.id))
    info = f"Ваша информация из БД:\n{chr(10).join(f'{i+1}) {h}' for i, h in enumerate(history))}"
    await message.answer(text=info)


@router.callback_query(IsSubscribeCallback())
async def subscribe_to_alerts(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=f"Теперь Вы будете каждые пять минут получать информацию о товаре с артикулом <b>{callback.data}</b>"
    )
    await state.set_state(state=WBStates.start_loop)
    await state.update_data(stop_loop="no")

    while True:
        await asyncio.sleep(settings.PERIOD_TIME)
        state_data = await state.get_data()
        if state_data.get("stop_loop") == "yes":
            await state.set_state(state=None)
            break
        wb = WBProduct()
        product_info = await wb.get_info(int(callback.data))
        await callback.message.answer(text=product_info)


@router.message(IsCancelSubscription(), StateFilter(WBStates.start_loop))
async def stop_subscription(message: Message, state: FSMContext):
    await state.update_data(stop_loop="yes")
    await message.answer(text="Подписка на все оповещения отменена")


@router.message(StateFilter(WBStates.get_info))
async def get_info_about_product(message: Message, state: FSMContext):
    item_id = message.text
    if item_id.isdigit():
        wb = WBProduct()
        product_info = await wb.get_info(int(item_id))
        if product_info:
            subscribe_kb = get_subscribe_keyboard(item_id)
            await message.answer(text=product_info, reply_markup=subscribe_kb)
            await WBCrud.add(
                user_tg_id=int(message.from_user.id),
                date_time=datetime.now(),
                item_number=int(item_id),
            )
        else:
            await message.answer(text="Информации по данному артикулу товара нет")
    else:
        await message.answer(text="Некорректное значение артикула товара")
    await state.clear()
