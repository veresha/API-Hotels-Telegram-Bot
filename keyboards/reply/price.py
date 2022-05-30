from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def chose_price() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('lowerprice', request_contact=True))
    return keyboard
