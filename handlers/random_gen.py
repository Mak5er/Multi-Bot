import asyncio
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import handlers.users as hu
from keyboards import keyboards as kb
from main import dp, _, bot
from middlewares.throttling_middleware import rate_limit


class GeneratePass(StatesGroup):
    pass_len = State()
    num_length = State()


@rate_limit(1)
@dp.message_handler(text=['🔐Generate password', '🔐Згенерувати пароль'])
async def password_generator_handler(message: types.Message):
    await message.answer(_("Please enter password length: "), reply_markup=kb.return_menu_keyboard())
    await GeneratePass.pass_len.set()


@dp.message_handler(state=GeneratePass.pass_len)
async def generate_password(message: types.Message, state: FSMContext):
    if message.text == _('📂Menu'):
        await state.finish()
        await hu.send_welcome(message)
        return
    pass_len = message.text
    if int(pass_len) >= 4001:
        await message.reply(_("Password can't be greater than 4000 symbols"))
        await state.finish()
        await GeneratePass.pass_len.set()
        return
    await state.finish()
    flag = True
    try:
        int(pass_len)

    except ValueError:
        flag = False

    if flag:
        chars = '+-*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

        lenght = int(pass_len)

        password = ""
        wait_message = await bot.send_message(message.chat.id, "⏳", reply_markup=types.ReplyKeyboardRemove())

        await asyncio.sleep(1)

        for i in range(lenght):
            password += random.choice(chars)

        await bot.delete_message(chat_id=message.chat.id, message_id=wait_message.message_id)

        await message.answer(_('Here are your password:\n\n `{password}`').format(password=password),
                             parse_mode='Markdown',
                             reply_markup=kb.return_select_keyboard())
    else:
        await message.answer(_("Please enter a number: "))
        await GeneratePass.pass_len.set()
        return


@dp.message_handler(text=['🔢Random number', '🔢Випадкове число'])
async def random_num_handler(message: types.Message):
    await message.answer(_("Hi enter range of numbers by -, or select one from examples."),
                         reply_markup=kb.return_numbers_keyboard())
    await GeneratePass.num_length.set()


@dp.message_handler(state=GeneratePass.num_length)
async def generate_num(message: types.Message, state: FSMContext):
    if message.text == _('📂Menu'):
        await state.finish()
        await hu.send_welcome(message)
        return
    try:
        wait_message = await bot.send_message(message.chat.id, "⏳", reply_markup=types.ReplyKeyboardRemove())

        await asyncio.sleep(1)

        first_num = int(message.text.split('-')[0])
        second_num = int(message.text.split('-')[1])
        number = random.randint(first_num, second_num)
        await state.finish()

        await bot.delete_message(chat_id=message.chat.id, message_id=wait_message.message_id)

        await message.answer(_('Your number is `{number}`').format(number=number), parse_mode='Markdown',
                             reply_markup=kb.return_select_keyboard())
    except:
        await message.answer(_('Please enter correct numbers: '))
