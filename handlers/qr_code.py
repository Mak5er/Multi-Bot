import asyncio
import os

import segno
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from middlewares.throttling_middleware import rate_limit
from segno import helpers

import handlers.users as hu
from keyboards import keyboards as kb
from main import dp, bot, _


class GenerateQRCode(StatesGroup):
    waiting_for_link_type = State()
    waiting_for_wifi_ssid = State()
    waiting_for_wifi_password = State()
    waiting_for_fg_color = State()
    waiting_for_bg_color = State()
    waiting_for_generate = State()

@rate_limit(1)
@dp.message_handler(text=["QR code", "QR код"])
async def get_url_type(message: types.Message):
    await message.answer(_("Choose the type of QR code:"), reply_markup=kb.return_qr_type_keyboard())
    await GenerateQRCode.waiting_for_link_type.set()


@dp.message_handler(state=GenerateQRCode.waiting_for_link_type)
async def process_link_type(message: types.Message, state: FSMContext):
    link_type = message.text
    if message.text == _('📂Menu'):
        await hu.send_welcome(message)
        await state.finish()
        return

    elif link_type == _("Simple QR code"):
        await message.answer(_("Enter URL:"), reply_markup=kb.return_menu_keyboard())
        await GenerateQRCode.waiting_for_fg_color.set()
    elif link_type == _("Wi-Fi QR-code"):
        await message.answer(_("Enter the Wi-Fi network name:"), reply_markup=kb.return_menu_keyboard())
        await GenerateQRCode.waiting_for_wifi_ssid.set()
    await state.update_data(link_type=link_type)


@dp.message_handler(state=GenerateQRCode.waiting_for_wifi_ssid)
async def process_wifi_ssid(message: types.Message, state: FSMContext):
    if message.text == _('📂Menu'):
        await hu.send_welcome(message)
        await state.finish()
        return
    wifi_ssid = message.text
    await message.answer(_("Enter Wi-Fi password:"), reply_markup=kb.return_menu_keyboard())
    await GenerateQRCode.waiting_for_wifi_password.set()
    await state.update_data(wifi_ssid=wifi_ssid)


@dp.message_handler(state=GenerateQRCode.waiting_for_wifi_password)
async def process_wifi_password(message: types.Message, state: FSMContext):
    if message.text == _('📂Menu'):
        await hu.send_welcome(message)
        await state.finish()
        return
    wifi_password = message.text
    await message.answer(_("Select the color of the QR code."), reply_markup=kb.return_color_keyboard())
    await GenerateQRCode.waiting_for_bg_color.set()
    await state.update_data(wifi_password=wifi_password)


@dp.message_handler(state=GenerateQRCode.waiting_for_fg_color)
async def fg_color(message: types.Message, state: FSMContext):
    if message.text == _('📂Menu'):
        await hu.send_welcome(message)
        await state.finish()
        return
    url = message.text
    await message.answer(_("Select the color of the QR code."), reply_markup=kb.return_color_keyboard())
    await GenerateQRCode.waiting_for_bg_color.set()
    await state.update_data(url=url)


@dp.message_handler(state=[GenerateQRCode.waiting_for_bg_color, GenerateQRCode.waiting_for_generate])
async def menu_handler(message: types.Message, state: FSMContext):
    if message.text == _('📂Menu'):
        await hu.send_welcome(message)
        await state.finish()
        return


@dp.callback_query_handler(lambda call: call.data.startswith('color_'), state=GenerateQRCode.waiting_for_bg_color)
async def bg_color(call: types.CallbackQuery, state: FSMContext):
    fg_color = call.data.split('_')[1]
    await call.message.edit_text(_("Now choose a background color."), reply_markup=kb.return_color_keyboard())
    await GenerateQRCode.waiting_for_generate.set()
    await state.update_data(fg_color=fg_color)


@dp.callback_query_handler(lambda call: call.data.startswith('color_'), state=GenerateQRCode.waiting_for_generate)
async def qenerate_qr(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    bg_color = call.data.split('_')[1]

    link_type = data.get('link_type')
    fg_color = data.get('fg_color')
    await state.finish()

    if bg_color == fg_color:
        await call.message.edit_text(_("You can't choose the same color twice! Choose the colors again."))
        await call.message.answer(_("Select the color of the QR code."), reply_markup=kb.return_color_keyboard())
        await GenerateQRCode.waiting_for_bg_color.set()
        await state.update_data(**data)
        return

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    wait_message = await bot.send_message(call.message.chat.id, "⏳", reply_markup=types.ReplyKeyboardRemove())

    await asyncio.sleep(1)

    qr_code_path = f"downloads/{call.message.from_user.id}_qr_code.png"


    if link_type == _("Simple QR code"):
        url = data.get('url')

        qrcode = segno.make(url, micro=False)
        qrcode.save(qr_code_path, scale=12, dark=fg_color, light=bg_color)

    elif link_type == _("Wi-Fi QR-code"):
        wifi_ssid = data.get('wifi_ssid')
        wifi_password = data.get('wifi_password')

        config = helpers.make_wifi_data(ssid=wifi_ssid, password=wifi_password, security='WPA')
        qrcode = segno.make(config, error='h')
        qrcode.save(qr_code_path, scale=12, dark=fg_color, light=bg_color)

    await bot.delete_message(chat_id=call.message.chat.id, message_id=wait_message.message_id)

    with open(qr_code_path, 'rb') as qr_code_file:
        await bot.send_photo(call.message.chat.id, qr_code_file, caption=_("Scan the QR code"),
                             reply_markup=kb.return_select_keyboard())

    os.remove(qr_code_path)
