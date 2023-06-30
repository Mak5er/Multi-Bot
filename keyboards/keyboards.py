from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from main import _

lang_keyboard = InlineKeyboardMarkup()
lang_keyboard.add(InlineKeyboardButton(text="Українська🇺🇦", callback_data="lang_uk"),
                  InlineKeyboardButton(text="English🇬🇧", callback_data="lang_en"))


def return_qr_type_keyboard():
    qr_type_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    simple_qr_button = types.KeyboardButton(_("Simple QR code"))
    wifi_qr_button = types.KeyboardButton(_("Wi-Fi QR-code"))
    menu_button = types.KeyboardButton(_('📂Menu'))
    qr_type_keyboard.row(simple_qr_button, wifi_qr_button)
    qr_type_keyboard.row(menu_button)
    return qr_type_keyboard


def return_select_keyboard():
    select_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    qr_button = KeyboardButton(text=_("QR code"))
    wt_button = KeyboardButton(text=_("🌦Weather"))
    nt_button = KeyboardButton(text=_("🎯Tasks"))
    pass_button = KeyboardButton(text=_("🔐Generate password"))
    random_num_button = KeyboardButton(text=_("🔢Random number"))
    select_keyboard.row(qr_button, wt_button, nt_button)
    select_keyboard.row(pass_button, random_num_button)
    return select_keyboard


def return_color_keyboard():
    color_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    red_button = types.InlineKeyboardButton(text="🟥", callback_data="color_red")
    orange_button = types.InlineKeyboardButton(text="🟧", callback_data="color_orange")
    yellow_button = types.InlineKeyboardButton(text="🟨", callback_data="color_yellow")
    green_button = types.InlineKeyboardButton(text="🟩", callback_data="color_green")
    blue_button = types.InlineKeyboardButton(text="🟦", callback_data="color_blue")
    purple_button = types.InlineKeyboardButton(text="🟪", callback_data="color_purple")
    black_button = types.InlineKeyboardButton(text="⬛️", callback_data="color_black")
    white_button = types.InlineKeyboardButton(text="⬜️", callback_data="color_white")
    brown_button = types.InlineKeyboardButton(text="🟫", callback_data="color_brown")
    color_keyboard.row(red_button, orange_button, yellow_button)
    color_keyboard.row(green_button, blue_button, purple_button)
    color_keyboard.row(black_button, white_button, brown_button)
    return color_keyboard


def return_location_keyboard():
    location_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    send_location_button = types.KeyboardButton(_('📍Set your location'), request_location=True)
    location_keyboard.add(send_location_button)
    return location_keyboard


def return_weather_or_forecast_keyboard():
    weather_or_forecast_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    get_weather_button = types.KeyboardButton(_('Current weather'))
    get_forecast_button = types.KeyboardButton(_('Forecast for tomorrow'))
    menu_button = types.KeyboardButton(_('📂Menu'))
    weather_or_forecast_keyboard.add(get_weather_button, get_forecast_button)
    weather_or_forecast_keyboard.add(menu_button)
    return weather_or_forecast_keyboard


def return_numbers_keyboard():
    numbers_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    z_h_button = types.KeyboardButton('0-99')
    z_t_button = types.KeyboardButton('0-999')
    z_tt_button = types.KeyboardButton('0-9999')
    z_ht_button = types.KeyboardButton('0-99999')
    z_m_button = types.KeyboardButton('0-999999')
    menu_button = types.KeyboardButton(_('📂Menu'))
    numbers_keyboard.row(z_h_button, z_t_button, z_tt_button)
    numbers_keyboard.row(z_ht_button, z_m_button)
    numbers_keyboard.row(menu_button)
    return numbers_keyboard


def return_menu_keyboard():
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton(_('📂Menu'))
    menu_keyboard.add(menu_button)
    return menu_keyboard
