from telebot.types import ReplyKeyboardMarkup


def district_choice(districts):
    buttons = districts
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard
