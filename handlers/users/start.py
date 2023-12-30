from loader import bot, dp, db
from aiogram import types
import asyncpg
from aiogram.types.web_app_info import WebAppInfo


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    telegramID = message.from_user.id
    check_id = await db.check_telegram_id(tg_id=telegramID)
    # print(check_id)
    if check_id:
        pass
    else:
        try:
            await db.add_user(
                telegram_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username,
            )
        except asyncpg.exceptions.UniqueViolationError:
            pass
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Web saxifam',
              web_app=WebAppInfo(url='https://axlidin.github.io/')))
    await message.answer('Web App!',
                           reply_markup=markup)

PRICE = {
    '1': [types.LabeledPrice(label='Item1', amount=100000)],
    '2': [types.LabeledPrice(label='Item2', amount=200000)],
    '3': [types.LabeledPrice(label='Item3', amount=300000)],
    '4': [types.LabeledPrice(label='Item4', amount=400000)],
    '5': [types.LabeledPrice(label='Item5', amount=500000)],
    '6': [types.LabeledPrice(label='Item6', amount=600000)]
}

@dp.message_handler(content_types='web_app_data')
async def buy_process(web_app_message):
    await bot.send_invoice(web_app_message.chat.id,
                           title='Laptop',
                           description='Description',
                           provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
                           currency='UZS',
                           need_email=True,
                           prices=PRICE[f'{web_app_message.web_app_data.data}'],
                           start_parameter='example',
                           payload='some_invoice')

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_process(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await bot.send_message(message.chat.id, 'Toʻlov muvaffaqiyatli boʻldi!')