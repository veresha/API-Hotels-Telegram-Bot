from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
import functools
import re
from users_info_storage.users_info_storage import users_info_dict
from work_with_api import testAPI

city_pattern = r'^\w+(?:[\s-]\w+)*$'
date_pattern = r'[2022+]\d+-[1-12]\d+-[1-31]\d+'


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
        user_id = message.from_user.id
        if re.fullmatch(city_pattern, message.text) and message.text.isdigit() is False:
            bot.send_message(message.from_user.id, f'Записал! Вы хотите отправиться в город {message.text}.'
                                                   '\nТеперь введите дату заселения в формате "гггг-мм-чч":')
            users_info_dict[message.from_user.id].append({'city': message.text})
            bot.set_state(message.from_user.id, UserState.check_in, message.chat.id)
            return True

    @decorator_check_info('Ошибка ввода, неправильно введена дата!')
    @bot.message_handler(state=UserState.check_in)
    def get_check_in(message: Message) -> bool:
        if re.fullmatch(date_pattern, message.text):
            bot.send_message(message.from_user.id, f'Записал! Дата заселения {message.text}. '
                                                   f'Теперь выберете дату выезда: ')
            users_info_dict[message.from_user.id].append({'check_in': message.text})
            bot.set_state(message.from_user.id, UserState.check_out, message.chat.id)
            return True

    @decorator_check_info('Ошибка ввода, неправильно введена дата!')
    @bot.message_handler(state=UserState.check_out)
    def get_check_out(message: Message) -> bool:
        if re.fullmatch(date_pattern, message.text):
            bot.send_message(message.from_user.id, f'Записал! Дата выселения {message.text}. Сколько отелей показать?')
            users_info_dict[message.from_user.id].append({'check_out': message.text})
            bot.set_state(message.from_user.id, UserState.hotels_num, message.chat.id)
            return True

    @decorator_check_info('Ошибка ввода, это должна быть цифра!')
    @bot.message_handler(state=UserState.hotels_num)
    def get_hotels_num(message: Message) -> bool:
        try:
            hotels_num = int(message.text)
        except ValueError:
            return False
        else:
            bot.send_message(message.from_user.id, f'Записал, выводим {hotels_num} отеля/ей. Сколько фото вывести?')
            users_info_dict[message.from_user.id].append({'hotels_num': hotels_num})
            bot.set_state(message.from_user.id, UserState.photos, message.chat.id)
            return True

    @decorator_check_info('Ошибка ввода, это должна быть цифра!')
    @bot.message_handler(state=UserState.photos)
    def get_photos_num(message: Message) -> bool:
        try:
            photos_num = int(message.text)
        except ValueError:
            return False
        else:
            bot.send_message(message.from_user.id, f'Загружаю {photos_num} отеля/ей')
            users_info_dict[message.from_user.id].append({'photos_num': photos_num})
            bot.set_state(message.from_user.id, UserState.work_with_api, message.chat.id)
            return True

    # testAPI.main()


if __name__ == '__main__':
    main()
