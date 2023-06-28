from aiogram import types

from keyboards import keyboards as kb
from main import dp, _
from services import DataBase

db = DataBase('services/users.db')


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await dp.bot.send_chat_action(message.chat.id, "typing")

    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_username = message.from_user.username

    await db.add_users(user_id, user_name, user_username)

    await message.reply(_("Hi! I'm your bot, Multitool."), reply_markup=kb.return_select_keyboard())
