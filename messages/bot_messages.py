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
