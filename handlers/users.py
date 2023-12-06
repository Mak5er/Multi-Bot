import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

import config
from keyboards import keyboards as kb
from main import dp, bot, _, update_info
from messages import bot_messages as bm
from middlewares.throttling_middleware import rate_limit
from services import DataBase

db = DataBase()

admin_id = config.admin_id

@rate_limit(1)
@dp.message_handler(commands=["start"])
@dp.message_handler(text=['📂Menu', '📂Меню'])
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")

    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_username = message.from_user.username

    await db.add_users(user_id, user_name, user_username)

    await message.reply(_("Hi! I'm your bot, Multitool."), reply_markup=kb.return_select_keyboard())

@rate_limit(1)
@dp.message_handler(text=["ℹ️INFO", "ℹ️ІНФО"])
async def info_handler(message: types.Message):
    await message.answer(bm.send_info(), reply_markup=kb.return_feedback_button())

@rate_limit(1)
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


@dp.callback_query_handler(lambda call: call.data == 'feedback')
@rate_limit(1)
async def feedback_handler(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(_('Please enter your message:'), reply_markup=kb.cancel_keyboard())
    await dp.current_state().set_state("send_feedback")
    await update_info(call.message)


@dp.message_handler(state="send_feedback")
async def feedback(message: types.Message, state: FSMContext):
    feedback_message = message.text
    feedback_message_id = message.message_id
    feedback_message_chat_id = message.chat.id
    user_id = message.from_user.id
    user_username = message.from_user.username

    if feedback_message == _("↩️Cancel"):
        await bot.send_message(message.chat.id,
                               _('Action canceled!'),
                               reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        await info_handler(message)
        return

    if user_username is not None:
        user = "@" + user_username
    else:
        user = user_id

    await state.finish()

    await bot.send_message(chat_id=admin_id, text=bm.feedback_message_send(user, feedback_message),
                           reply_markup=kb.feedback_answer(feedback_message_id, feedback_message_chat_id),
                           parse_mode="Markdown")

    await message.answer(
        _("Your message *{feedback_message_id}* sent!").format(feedback_message_id=feedback_message_id),
        reply_markup=types.ReplyKeyboardRemove())
    await update_info(message)
