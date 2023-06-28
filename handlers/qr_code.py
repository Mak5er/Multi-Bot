import os

import segno
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from segno import helpers

from keyboards import keyboards as kb
from main import dp, bot, _


class GenerateQRCode(StatesGroup):
    waiting_for_link_type = State()
    waiting_for_wifi_ssid = State()
    waiting_for_wifi_password = State()
    waiting_for_fg_color = State()
    waiting_for_bg_color = State()
    waiting_for_generate = State()


@dp.message_handler(text=[_("QR code")])
async def get_url_type(message: types.Message):
    await message.answer(_("Choose the type of QR code:"), reply_markup=kb.return_qr_type_keyboard())
    await GenerateQRCode.waiting_for_link_type.set()


@dp.message_handler(state=GenerateQRCode.waiting_for_link_type)
async def process_link_type(message: types.Message, state: FSMContext):
    link_type = message.text
    if link_type == _("Simple QR code"):
        await message.answer(_("Enter URL:"), reply_markup=types.ReplyKeyboardRemove())
        await GenerateQRCode.waiting_for_fg_color.set()
    elif link_type == _("Wi-Fi QR-code"):
        await message.answer(_("Enter the Wi-Fi network name:"))
        await GenerateQRCode.waiting_for_wifi_ssid.set()
    await state.update_data(link_type=link_type)


@dp.message_handler(state=GenerateQRCode.waiting_for_wifi_ssid)
async def process_wifi_ssid(message: types.Message, state: FSMContext):
    wifi_ssid = message.text
    await message.answer(_("Enter Wi-Fi password:"))
    await GenerateQRCode.waiting_for_wifi_password.set()
    await state.update_data(wifi_ssid=wifi_ssid)


@dp.message_handler(state=GenerateQRCode.waiting_for_wifi_password)
async def process_wifi_password(message: types.Message, state: FSMContext):
    wifi_password = message.text
    await message.answer(_("Select the color of the QR code."), reply_markup=kb.return_color_keyboard())
    await GenerateQRCode.waiting_for_bg_color.set()
    await state.update_data(wifi_password=wifi_password)


@dp.message_handler(state=GenerateQRCode.waiting_for_fg_color)
async def fg_color(message: types.Message, state: FSMContext):
    url = message.text
    await message.answer(_("Select the color of the QR code."), reply_markup=kb.return_color_keyboard())
    await GenerateQRCode.waiting_for_bg_color.set()
    await state.update_data(url=url)


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

    if link_type == _("Simple QR code"):
        url = data.get('url')
        qr_code_path = f"downloads/{call.message.from_user.id}_qr_code.png"

        # Генерація QR-коду
        qrcode = segno.make(url, micro=False)
        qrcode.save(qr_code_path, scale=12, dark=fg_color, light=bg_color)

    elif link_type == _("Wi-Fi QR-code"):
        wifi_ssid = data.get('wifi_ssid')
        wifi_password = data.get('wifi_password')
        qr_code_path = f"downloads/{call.message.from_user.id}_qr_code.png"

        # Генерація Wi-Fi QR-коду
        config = helpers.make_wifi_data(ssid=wifi_ssid, password=wifi_password, security='WPA')
        qrcode = segno.make(config, error='h')
        qrcode.save(qr_code_path, scale=12, dark=fg_color, light=bg_color)

    # Видалення попереднього повідомлення
    await bot.delete_message(call.message.chat.id, call.message.message_id)

    # Відправлення QR-коду користувачеві
    with open(f"downloads/{call.message.from_user.id}_qr_code.png", 'rb') as qr_code_file:
        await bot.send_photo(call.message.chat.id, qr_code_file, caption=_("Scan the QR code"),
                             reply_markup=kb.return_select_keyboard())

    os.remove(f"downloads/{call.message.from_user.id}_qr_code.png")
