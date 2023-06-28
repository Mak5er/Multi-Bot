from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

from main import _


def return_qr_type_keyboard():
    qr_type_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    simple_qr_button = types.KeyboardButton(_("Simple QR code"))
    wifi_qr_button = types.KeyboardButton(_("Wi-Fi QR-code"))
    qr_type_keyboard.row(simple_qr_button, wifi_qr_button)
    return qr_type_keyboard


def return_select_keyboard():
    select_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    qr_button = KeyboardButton(_("QR code"))
    yt_button = KeyboardButton(_("Скачать"))
    select_keyboard.row(qr_button, yt_button )
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


def menu():
    download_button = KeyboardButton('Скачать')
    menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu_kb.add(download_button)
    return menu_kb


def back():
    button_back = KeyboardButton('Отмена')
    back_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    back_kb.add(button_back)
    return back_kb


def make_keyboards(url):
    inline_kb1 = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Лучшее качество до 720p(с звуком).', callback_data=f'best_with_audio|{url}')
    button2 = InlineKeyboardButton('Лучшее качество(без звука).', callback_data=f'best_video|{url}')
    button3 = InlineKeyboardButton('Звук в лучшем качестве.', callback_data=f'best_audio|{url}')
    button4 = InlineKeyboardButton('Отмена', callback_data=f'cancel')
    inline_kb1.add(button)
    inline_kb1.add(button2)
    inline_kb1.add(button3)
    inline_kb1.add(button4)
    return inline_kb1
