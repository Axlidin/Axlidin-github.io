import logging

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from loader import dp, bot, db
from aiogram.dispatcher.filters import Text

from states.shop_states import SHOPPING

@dp.message_handler(user_id=5419118871, commands=["cancel"], state=SHOPPING)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Siz mahsulot yaratishni bekor qildingiz")
    await state.reset_state()

@dp.message_handler(text="Add", chat_id=5419118871)
async def Add_products(message: types.Message):
    await message.answer("<b>Mahsulot qo'shish:</b>\nMahsulot nomini kiritig yoki /cancel bosing")
    await SHOPPING.next()

@dp.message_handler(state=SHOPPING.Mahsulot_nomi)
async def Product_name(message: types.Message, state: FSMContext):
    Mahsulot_nomi = message.text
    print(Mahsulot_nomi)
    await state.update_data(
        {"Mahsulot_nomi": Mahsulot_nomi}
    )
    await SHOPPING.next()
    await message.answer("Mahsulotning rasmini yuboring yoki /cancel bosing")

@dp.message_handler(state=SHOPPING.Mahsulot_rasmi, content_types=types.ContentTypes.PHOTO)
async def Photo(message: types.Message, state: FSMContext):
    Mahsulot_rasmi = message.photo[-1].file_id
    # print(Mahsulot_rasmi)
    data = await state.get_data()
    Mahsulot_nomi = data.get('Mahsulot_nomi')
    await state.update_data(
        {"Mahsulot_rasmi": Mahsulot_rasmi}
    )
    await SHOPPING.next()
    await message.answer_photo(photo=Mahsulot_rasmi, caption=f"<b>{Mahsulot_nomi}</b>\n"
                         f"Mahsulot narxini UZS <b>({100000:,}) so'm</b>"
                         f" ko'rinishida yuboring yoki /cancel bosing")

@dp.message_handler(lambda message: not message.text.isdigit(), state=SHOPPING.Mahsulot_narhi)
async def process_price_invalid(message: types.Message):
    """
    If price is invalid
    """
    return await message.reply("Iltimos faqat raqam kiriting yoki /cancel bosing")

@dp.message_handler(lambda message: message.text.isdigit(), state=SHOPPING.Mahsulot_narhi)
async def Price(message: types.Message, state: FSMContext):
    Mahsulot_narhi = message.text
    Mahsulot_narhi = int(Mahsulot_narhi)
    print(Mahsulot_narhi)
    await state.update_data(
        {"Mahsulot_narhi": Mahsulot_narhi}
    )

    # ma'lumotlarni qayta o'qish
    data = await state.get_data()
    Mahsulot_nomi = data.get("Mahsulot_nomi")
    Mahsulot_narhi = data.get("Mahsulot_narhi")

    msg = f"Mahsulot nomi ---- <b>{Mahsulot_nomi}</b>\n"
    msg += f"Mahsulot narhi ---- <b>{Mahsulot_narhi:,}</b> so'm\n"
    await message.answer(f"Mahsulot do'koningizga qo'shildi.\n{msg}")
    await state.finish()  # malumotlar ochib ketadi
    try:
        await db.add_product(
                            Mahsulot_nomi=data['Mahsulot_nomi'],
                            Mahsulot_narhi=str(data['Mahsulot_narhi']),
                            Mahsulot_rasmi=data['Mahsulot_rasmi']),

    except asyncpg.exceptions.UniqueViolationError:
        await state.reset_state(with_data=True)