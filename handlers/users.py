import asyncio

from aiogram import types

from keyboards import keyboards as kb
from main import dp, bot, _
from messages import bot_messages as bm
from services import DataBase

db = DataBase('services/users.db')


@dp.message_handler(commands=["start"])
@dp.message_handler(text=['📂Menu', '📂Меню'])
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")

    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_username = message.from_user.username

    await db.add_users(user_id, user_name, user_username)

    await message.reply(_("Hi! I'm your bot, Multitool."), reply_markup=kb.return_select_keyboard())


@dp.message_handler(text=["ℹ️INFO", "ℹ️ІНФО"])
async def info_handler(message: types.Message):
    await message.answer(bm.send_info())


@dp.message_handler(commands=['language'])
async def change_lang(message: types.Message):
    user_id = message.from_user.id

    await bot.send_chat_action(user_id, 'typing')

    wait_message = await bot.send_message(message.chat.id, "⏳", reply_markup=types.ReplyKeyboardRemove())

    await asyncio.sleep(1)

    await bot.delete_message(chat_id=message.chat.id, message_id=wait_message.message_id)

    await message.answer(_("Please choose your language!"), reply_markup=kb.lang_keyboard,
                         parse_mode="Markdown")


@dp.callback_query_handler(lambda call: call.data.startswith('lang_'))
async def language_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    language = call.data.split('_')[1]

    await db.set_language(user_id, language)

    await bot.send_chat_action(user_id, 'typing')
    await call.message.edit_text(text=bm.choose_lan(language), reply_markup=None)
