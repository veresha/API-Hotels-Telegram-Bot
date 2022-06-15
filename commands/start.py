from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
import functools
from loguru import logger
import re


def decorator_check_info(text):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped_wrapper(message):
            bot.send_message(message.from_user.id, text)
            if not func():
                bot.send_message(message.from_user.id, text)
        return wrapped_wrapper
    return wrapper


@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    bot.send_message(
        message.from_user.id,
        "Привет, в какой город хотите отправиться?"
    )


@decorator_check_info('Ошибка ввода, такого города не знаю!')
@bot.message_handler(state=UserState.city)
def get_city(message: Message) -> bool:
    city_pattern = r'\w+'
    if re.fullmatch(city_pattern, message.text):
        bot.send_message(message.from_user.id, 'Записал! Теперь введите дату в формате "Число/Месяц/Год":')
        bot.set_state(message.from_user.id, UserState.city, message.chat.id)

        # with bot(message.from_user.id, message.chat.id) as data:
        #     data['city'] = message.text.lower()
        return True


@decorator_check_info('Ошибка ввода, неправильно введена дата!')
@bot.message_handler(state=UserState.date)
def get_date(message: Message) -> bool:
    date_pattern = r'\d+/\d+/\d+'
    if re.fullmatch(date_pattern, message.text):
        bot.send_message(message.from_user.id, 'Записал! Теперь выберете стоимость:')
        bot.set_state(message.from_user.id, UserState.date, message.chat.id)

        # with bot(message.from_user.id, message.chat.id) as data:
        #     data['date'] = message.text
        return True

