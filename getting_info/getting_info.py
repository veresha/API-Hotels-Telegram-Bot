from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
import functools
import re
from users_info_storage.users_info_storage import users_info_dict

city_pattern = r'^\w+(?:[\s-]\w+)*$'
date_pattern = r'[1-31]\d+/[1-12]\d+/\d+'
new_user_id = 1


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
        if re.fullmatch(city_pattern, message.text) and message.text.isdigit() is False:
            bot.send_message(message.from_user.id, f'Записал! Вы хотите отправиться в город {message.text}.'
                                                   '\nТеперь введите дату заселения в формате "Число/Месяц/Год":')
            users_info_dict[new_user_id] = [{'city': message.text}]
            bot.set_state(message.from_user.id, UserState.check_in, message.chat.id)
            return True

    @decorator_check_info('Ошибка ввода, неправильно введена дата!')
    @bot.message_handler(state=UserState.check_in)
    def get_check_in(message: Message) -> bool:
        if re.fullmatch(date_pattern, message.text):
            bot.send_message(message.from_user.id, f'Записал! Дата заселения {message.text}. '
                                                   f'Теперь выберете дату выезда: ')
            users_info_dict[new_user_id] += [{'check_in': message.text}]
            bot.set_state(message.from_user.id, UserState.check_out, message.chat.id)
            return True

    @decorator_check_info('Ошибка ввода, неправильно введена дата!')
    @bot.message_handler(state=UserState.check_out)
    def get_check_out(message: Message) -> bool:
        if re.fullmatch(date_pattern, message.text):
            bot.send_message(message.from_user.id, f'Записал! Дата выселения {message.text}. Теперь выберете стоимость:'
                                                   '\n/lowprice - дешёвые отели,'
                                                   '\n/highprice - дорогие отели,'
                                                   '\n/bestdeal - лучшее предложение')
            users_info_dict[new_user_id] += [{'check_out': message.text}]
            bot.set_state(message.from_user.id, UserState.hotel_price, message.chat.id)
            return True

    # @decorator_check_info('Ошибка ввода, это должна быть цифра!')
    # @bot.message_handler(state=UserState.hotels_num)
    # def get_hotels_num(message: Message) -> bool:
    #     try:
    #         hotels_num = int(message.text)
    #     except ValueError:
    #         return False
    #     else:
    #         bot.send_message(message.from_user.id, f'Загружаю {hotels_num} отелей')
    #         users_info_dict[new_user_id] += [{'hotels_num': hotels_num}]
    #         bot.set_state(message.from_user.id, UserState.photos, message.chat.id)
    #         return True


if __name__ == '__main__':
    main()
