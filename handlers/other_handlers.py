from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from filters import IsGetProductInfo
from api_requests import WBProduct
from keyboards import get_subscribe_keyboard


class ProductStates(StatesGroup):
    get_info = State()


router: Router = Router()


@router.message(IsGetProductInfo())
async def input_product_item(message: Message, state: FSMContext):
    await state.set_state(state=ProductStates.get_info)
    await message.answer(text="Введите артикул товара")


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
        else:
            await message.answer(text="Информации по данному артикулу товара нет")
    else:
        await message.answer(text="Некорректное значение артикула товара")
    await state.clear()
