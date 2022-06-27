from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
import functools
import re
from users_info_storage.users_info_storage import users_info_dict
from work_with_api.work_with_api import get_city_districts, get_hotels
from telebot.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from keyboards.reply.district_choice import district_choice

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
    def get_city(message: Message) -> None:
        city_districts = get_city_districts(message.text)
        if city_districts:
            keyboard = district_choice(city_districts.keys())
            bot.send_message(message.from_user.id, f'Вы выбрали город {message.text}.'
                                                   f'\nВыберите район:', reply_markup=keyboard)
            bot.set_state(message.from_user.id, UserState.choice_district, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Такого города не знаю.')

    @bot.message_handler(state=UserState.choice_district)
    def choice_district(message: Message):
        users_info_dict[message.from_user.id].append({'city': message.text})
        bot.send_message(message.from_user.id, f'Записал! Вы выбрали {message.text}.'
                                               '\nТеперь выберите дату заселения, либо введите в формате "гггг-мм-чч":',
                         reply_markup=ReplyKeyboardRemove())
        city_districts = get_city_districts(message.text)
        users_info_dict[message.from_user.id].append({'destination_id': city_districts[message.text]})
        bot.set_state(message.from_user.id, UserState.check_in, message.chat.id)

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
            bot.send_message(message.from_user.id, f'Записал, выводим {hotels_num} отеля/ей. ')
                                                   #f'Сколько фото каждого отеля нужно?')
            users_info_dict[message.from_user.id].append({'hotels_num': hotels_num})
            bot.set_state(message.from_user.id, UserState.photos, message.chat.id)
            get_hotels(message)
            return True

    # @decorator_check_info('Ошибка ввода, это должна быть цифра!')
    # @bot.message_handler(state=UserState.photos)
    # def get_photos_num(message: Message) -> bool:
    #     try:
    #         photos_num = int(message.text)
    #     except ValueError:
    #         return False
    #     else:
    #         bot.send_message(message.from_user.id, f'Загружаю')
    #         users_info_dict[message.from_user.id].append({'photos_num': photos_num})
    #         return True


if __name__ == '__main__':
    main()
