from main import _


def choose_lan(language):
    if language == "uk":
        return """Ви обрали українську мову🇺🇦!
Ви завжди можете змінити мову написавши /language
Тепер знову натисніть /start
"""
    elif language == "en":
        return """You have selected English🇬🇧!
You can always change the language by writing /language
Now click /start again
"""


def send_info():
    return _("""🤖 This is a multi-tasking bot that can perform a variety of tasks. Here is a list of available functions:

️/start - start interaction with the bot
QR code - generate a QR code
🔢Random number - generate a random number
🔐Generate password - generate a random password
🎯Tasks - create and schedule tasks
🌦Weather - view the weather""")
