from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
from filters import IsGetProductInfo, IsGetWBHistory
from api_requests import WBProduct
from keyboards import get_subscribe_keyboard
from database.crud import WBCrud


class ProductStates(StatesGroup):
    get_info = State()


router: Router = Router()


@router.message(IsGetProductInfo())
async def input_product_item(message: Message, state: FSMContext):
    await state.set_state(state=ProductStates.get_info)
    await message.answer(text="Введите артикул товара")


@router.message(IsGetWBHistory())
async def get_wb_info_from_db(message: Message):
    history = await WBCrud.get_last_five_records(int(message.from_user.id))
    info = "Ваша информация из БД:\n"
    info += "\n".join(f"{i+1}) {h}" for i, h in enumerate(history))
    await message.answer(text=info)


@router.message(StateFilter(ProductStates.get_info))
async def get_info_about_product(message: Message, state: FSMContext):
    item_id = message.text
    if item_id.isdigit():
        wb = WBProduct()
        product_info = await wb.get_info(int(item_id))
        res_info = "\n".join(f"{k}{val}" for k, val in product_info.items())
        if res_info:
            subscribe_kb = get_subscribe_keyboard()
            await message.answer(text=res_info, reply_markup=subscribe_kb)
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
