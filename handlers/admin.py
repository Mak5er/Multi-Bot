from main import dp, bot
from aiogram import types
from config import admin_id


@dp.message_handler(user_id=admin_id, commands=['download_db'])
async def download_db(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    db_file = 'services/jokes.db'
    with open(db_file, 'rb') as file:
        await bot.send_document(message.chat.id, file)
