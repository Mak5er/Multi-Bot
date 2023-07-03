from aiogram import types
import asyncio

from messages import bot_messages as bm
from keyboards import keyboards as kb
from main import dp, bot, _
from services import DataBase

db = DataBase('services/users.db')


@dp.message_handler(commands=["start"])
@dp.message_handler(text=['📂Menu', '📂Меню'])
async def send_welcome(message: types.Message):
    await dp.bot.send_chat_action(message.chat.id, "typing")

    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_username = message.from_user.username

    await db.add_users(user_id, user_name, user_username)

    await message.reply(_("Hi! I'm your bot, Multitool."), reply_markup=kb.return_select_keyboard())


@dp.message_handler(commands=['language'])
async def change_lang(message: types.Message):
    user_id = message.from_user.id

    await bot.send_chat_action(user_id, 'typing')
    await asyncio.sleep(0.5)

    await message.reply(_("Please choose your language!"), reply_markup=kb.lang_keyboard, parse_mode="Markdown")


@dp.callback_query_handler(lambda call: call.data.startswith('lang_'))
async def language_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    language = call.data.split('_')[1]
    await bot.send_chat_action(user_id, 'typing')
    await asyncio.sleep(0.5)
    await call.message.edit_text(text=bm.choose_lan(language), reply_markup=None)

    await db.set_language(user_id, language)
