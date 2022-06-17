from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
import functools
import re
import json

data = dict()
data['availability_of_information'] = False
city_pattern = r'^\w+(?:[\s-]\w+)*$'
date_pattern = r'[1-31]\d+/[1-12]\d+/\d+'


def decorator_check_info(text):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped_wrapper(message, *args, **kwargs):
            if not func(message, *args, **kwargs):
                bot.send_message(message.from_user.id, text)
        return wrapped_wrapper
    return wrapper


def main():
    @bot.message_handler(state=UserState.city)
    @decorator_check_info('Ошибка ввода, такого города не знаю!')
    def get_city(message: Message) -> bool:
        # city_pattern = r'^\w+(?:[\s-]\w+)*$'
        if re.fullmatch(city_pattern, message.text) and message.text.isdigit() is False:
            bot.send_message(message.from_user.id, f'Записал! Вы хотите отправиться в город {message.text}.'
                                                   '\nТеперь введите дату заселения в формате "Число/Месяц/Год":')
            data['city'] = message.text
            bot.set_state(message.from_user.id, UserState.arrival_date, message.chat.id)
            return True

    @decorator_check_info('Ошибка ввода, неправильно введена дата!')
    @bot.message_handler(state=UserState.arrival_date)
    def get_date(message: Message) -> bool:
        # date_pattern = r'[1-31]\d+/[1-12]\d+/\d+'
        if re.fullmatch(date_pattern, message.text):
            bot.send_message(message.from_user.id, f'Записал! Дата заселения {message.text}. '
                                                   f'Теперь выберете дату выезда: ')
            data['arrival_date'] = message.text
            bot.set_state(message.from_user.id, UserState.date_of_departure, message.chat.id)
            return True

    @decorator_check_info('Ошибка ввода, неправильно введена дата!')
    @bot.message_handler(state=UserState.date_of_departure)
    def get_date(message: Message) -> bool:
        # date_pattern = r'[1-31]\d+/[1-12]\d+/\d+'
        if re.fullmatch(date_pattern, message.text):
            bot.send_message(message.from_user.id, f'Записал! Дата выселения {message.text}. Теперь выберете стоимость: '
                                                   '\n/lowprice - дешёвые отели,'
                                                   '\n/highprice - дорогие отели,'
                                                   '\n/bestdeal - лучшее предложение')
            data['date_of_departure'] = message.text
            data['availability_of_information'] = True
            with open('user_info.json', 'w', encoding='utf-8') as user_data:
                json.dump(data, user_data, ensure_ascii=False)
            bot.set_state(message.from_user.id, UserState.hotel_price, message.chat.id)
            return True

    # data['availability_of_information'] = True
    # print(data)


if __name__ == '__main__':
    main()
