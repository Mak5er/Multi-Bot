from aiogram import types
from main import bot, dp, _
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from services import DataBase
from keyboards import keyboards as kb

db = DataBase('services/users.db')


class Notes(StatesGroup):
    add_note = State()


async def return_notes(message, user_id):
    notes = await db.get_notes(user_id)

    if notes:
        response = _("*Your tasks:*\n\n")
        notes_keyboard = types.InlineKeyboardMarkup()
        i = 1

        for note in notes:
            note_text = note[1][:30] + "..." if len(note[1]) > 30 else note[1]
            response += f"#{i} - _{note_text}_\n"
            i += 1

            note_text_button = types.InlineKeyboardButton(text=f"{note_text}", callback_data=f"manage_note:{note[0]}")
            notes_keyboard.add(note_text_button)

        add_button = types.InlineKeyboardButton(text=_("➕Add task"), callback_data="add_note")
        notes_keyboard.add(add_button)
        await bot.send_message(chat_id=message.chat.id, text=response, reply_markup=notes_keyboard,
                               parse_mode='Markdown')
    else:
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text=_("➕Add task"), callback_data="add_note")
        keyboard.add(button)

        await bot.send_message(chat_id=message.chat.id, text=_("You haven't tasks."), reply_markup=keyboard)


@dp.message_handler(text=['🎯Tasks', '🎯Задачі'])
async def list_notes(message: types.Message):
    user_id = message.from_user.id

    await message.reply('Hi, here are your notes!', reply_markup=kb.return_menu_keyboard())
    await return_notes(message, user_id)


@dp.callback_query_handler(lambda call: call.data.startswith('manage_note:'))
async def manage_note_callback(call: types.CallbackQuery):
    note_id = int(call.data.split(':')[1])

    note = await db.get_note(note_id)

    if note:
        keyboard = types.InlineKeyboardMarkup()
        delete_button = types.InlineKeyboardButton(text=_("❌Delete"), callback_data=f"delete_note:{note_id}")
        back_button = types.InlineKeyboardButton(text=_("🔙Back"), callback_data="back_to_list")
        keyboard.row(delete_button)
        keyboard.row(back_button)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=note[0],
                                    reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data == 'add_note')
async def add_note_callback(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=_("Enter your task:"))
    await bot.answer_callback_query(call.id)
    await Notes.add_note.set()


@dp.callback_query_handler(lambda call: call.data.startswith('delete_note:'))
async def delete_note_callback(call: types.CallbackQuery):
    note_id = int(call.data.split(':')[1])
    message = call.message
    user_id = call.from_user.id

    await db.delete_note(note_id)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=_("Task deleted."))
    await return_notes(message, user_id)
    await bot.answer_callback_query(call.id)


@dp.callback_query_handler(lambda call: call.data == 'back_to_list')
async def back_to_list_callback(call: types.CallbackQuery):
    user_id = call.from_user.id
    message = call.message

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await return_notes(message, user_id)
    await bot.answer_callback_query(call.id)


@dp.message_handler(state=Notes.add_note)
async def add_note_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    note_text = message.text

    await db.add_note(user_id, note_text)

    await message.reply(_("Task added."))
    await return_notes(message, user_id)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
