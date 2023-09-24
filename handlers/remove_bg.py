import asyncio
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from PIL import Image
from rembg import remove

import handlers.users as hu
from keyboards import keyboards as kb
from main import _, bot, dp
from middlewares.throttling_middleware import rate_limit


class RemoveBG(StatesGroup):
    waiting_for_image = State()

@rate_limit(1)
@dp.message_handler(text=["🖼️Remove Background", "🖼️Прибрати фон"])
async def remove_bg_handler(message: types.Message):
    await message.answer(_("Please send me a photo🖼️"), reply_markup=kb.return_menu_keyboard())
    await RemoveBG.waiting_for_image.set()

@dp.message_handler(content_types=[ ContentType.TEXT, ContentType.PHOTO ], state=RemoveBG.waiting_for_image)
async def remove_bg(message: types.Message, state: FSMContext):
    if message.photo:
        await state.finish()
        largest_photo = message.photo[-1]
        
        file_id = largest_photo.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        file_extension = os.path.splitext(file_path)[-1]
        downloaded_file_path = f'downloads/{file_id}{file_extension}'
        output_path = f"{downloaded_file_path}_rembg.png"

        wait_message = await bot.send_message(message.chat.id, "⏳", reply_markup=types.ReplyKeyboardRemove())

        await asyncio.sleep(1)

        await bot.download_file(file_path, downloaded_file_path)

        input = Image.open(downloaded_file_path)
        output = remove(input)
        output.save(output_path)

        os.remove(downloaded_file_path)

        await bot.delete_message(chat_id=message.chat.id, message_id=wait_message.message_id)

        await bot.send_document(chat_id=message.chat.id, document=open(output_path, 'rb'), reply_markup=kb.return_select_keyboard())

        os.remove(output_path)

    else:
        if message.text == _('📂Menu'):
            await hu.send_welcome(message)
            await state.finish()
            return


