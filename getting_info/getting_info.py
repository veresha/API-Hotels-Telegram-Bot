from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
import functools
from users_info_storage.users_info_storage import users_info_dict
from work_with_api.work_with_api import get_city_districts, get_hotels, get_photos
from telebot.types import ReplyKeyboardRemove
from keyboards.reply.district_choice import district_choice
from keyboards.inline.calendar import MyStyleCalendar
from datetime import datetime, timedelta, date


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
        bot.send_message(message.from_user.id, f'Записал! Вы выбрали {message.text}.',
                         reply_markup=ReplyKeyboardRemove())
        city_districts = get_city_districts(message.text)
        users_info_dict[message.from_user.id].append({'destination_id': city_districts[message.text]})
        bot.set_state(message.from_user.id, UserState.check_in, message.chat.id)
        get_check_in(message)

    @bot.message_handler(state=UserState.check_in)
    def get_check_in(message: Message):
        calendar, step = MyStyleCalendar(locale='ru', min_date=date.today()).build()
        bot.send_message(message.from_user.id, f'Теперь выберите дату заселения:',
                         reply_markup=calendar)

        @bot.callback_query_handler(state=UserState.check_in, func=MyStyleCalendar.func())
        def callback_check_in(callback):
            result, key, step = MyStyleCalendar(
                locale='ru', min_date=date.today()).process(callback.data)
            if not result and key:
                bot.edit_message_text(f"Выберите дату заселения:",
                                      callback.message.chat.id,
                                      callback.message.message_id,
                                      reply_markup=key)
            elif result:
                bot.edit_message_text(f"Дата заселения {result}.",
                                      callback.message.chat.id,
                                      callback.message.message_id)
                users_info_dict[message.from_user.id].append({'check_in': str(result)})
                bot.set_state(message.from_user.id, UserState.check_out, message.chat.id)
                get_check_out(message)

    @bot.message_handler(state=UserState.check_out)
    def get_check_out(message: Message):
        check_in_date = datetime.strptime(
            users_info_dict[message.from_user.id][3]['check_in'], "%Y-%m-%d").date()
        calendar, step = MyStyleCalendar(locale='ru', min_date=check_in_date).build()
        bot.send_message(message.from_user.id, f'Теперь выберите дату выезда:',
                         reply_markup=calendar)

        @bot.callback_query_handler(func=MyStyleCalendar.func())
        def callback_check_out(callback):
            result, key, step = MyStyleCalendar(
                locale='ru', min_date=check_in_date + timedelta(days=1)).process(callback.data)
            if not result and key:
                bot.edit_message_text(f"Выберите дату выезда:",
                                      callback.message.chat.id,
                                      callback.message.message_id,
                                      reply_markup=key)
            elif result:
                bot.edit_message_text(f"Записал! Дата выезда {result}.",
                                      callback.message.chat.id,
                                      callback.message.message_id)
                users_info_dict[message.from_user.id].append({'check_out': str(result)})
                bot.send_message(message.from_user.id, "Сколько отелей показать?(0 - 10)")
                bot.set_state(message.from_user.id, UserState.hotels_num, message.chat.id)

    @bot.message_handler(state=UserState.hotels_num)
    @decorator_check_info('Ошибка ввода, это должна быть цифра от 1 до 10!')
    def get_hotels_num(message: Message) -> bool:
        try:
            hotels_num = int(message.text)
        except ValueError:
            return False
        else:
            if hotels_num in range(1, 11):
                bot.send_message(message.from_user.id, f'Записал, выводим {hotels_num} отеля/ей.')
                users_info_dict[message.from_user.id].append({'hotels_num': hotels_num})
                if users_info_dict[message.from_user.id][0]["hotels_price"] != "BEST_SELLER":
                    bot.send_message(message.from_user.id, "Сколько фото каждого отеля показать?(0 - 10)")
                    bot.set_state(message.from_user.id, UserState.photos_num, message.chat.id)
                else:
                    bot.send_message(message.from_user.id, "Какая минимальная цена за ночь?")
                    bot.set_state(message.from_user.id, UserState.min_price, message.chat.id)
                return True

    @bot.message_handler(state=UserState.min_price)
    @decorator_check_info('Ошибка ввода, это должна быть цифра больше 0!')
    def get_min_price(message: Message):
        try:
            min_price = int(message.text)
        except ValueError:
            return False
        else:
            if min_price > 0:
                bot.send_message(message.from_user.id, f'Записал, минимальная цена {message.text}$.\n'
                                                       f'Какая максимальная цена за ночь?')
                users_info_dict[message.from_user.id].append({'min_price': min_price})
                bot.set_state(message.from_user.id, UserState.max_price, message.chat.id)
                return True

    @bot.message_handler(state=UserState.max_price)
    @decorator_check_info('Ошибка ввода, это должна быть цифра больше минимальной цены!')
    def get_max_price(message: Message):
        try:
            max_price = int(message.text)
        except ValueError:
            return False
        else:
            if max_price > users_info_dict.get(message.from_user.id)[6]['min_price']:
                bot.send_message(message.from_user.id, f'Записал, максмальная цена {message.text}$.\n'
                                                       f'Какое минимальное расстояние до центра?')
                users_info_dict[message.from_user.id].append({'max_price': max_price})
                bot.set_state(message.from_user.id, UserState.min_dist, message.chat.id)
                return True

    @bot.message_handler(state=UserState.min_dist)
    @decorator_check_info('Ошибка ввода, это должна быть цифра больше 0!')
    def get_min_dist(message: Message):
        try:
            min_dist = int(message.text)
        except ValueError:
            return False
        else:
            if min_dist >= 0:
                bot.send_message(message.from_user.id, f'Записал, минимальное расстояние {message.text} км.\n'
                                                       f'Какое максимальное расстояние до центра?')
                users_info_dict[message.from_user.id].append({'min_dist': min_dist})
                bot.set_state(message.from_user.id, UserState.max_dist, message.chat.id)
                return True

    @bot.message_handler(state=UserState.max_dist)
    @decorator_check_info('Ошибка ввода, это должна быть цифра больше минимального расстояния!')
    def get_max_dist(message: Message):
        try:
            max_dist = int(message.text)
        except ValueError:
            return False
        else:
            if max_dist > users_info_dict[message.from_user.id][8]['min_dist']:
                bot.send_message(message.from_user.id, f'Записал, максимальное расстояние {message.text} км.\n'
                                                       f'Сколько фото каждого отеля показать?(0 - 10)')
                users_info_dict[message.from_user.id].append({'max_dist': max_dist})
                bot.set_state(message.from_user.id, UserState.photos_num, message.chat.id)
                return True

    @bot.message_handler(state=UserState.photos_num)
    @decorator_check_info('Ошибка ввода, это должна быть цифра от 0 до 10!')
    def get_photos_num(message: Message) -> bool:
        try:
            photos_num = int(message.text)
        except ValueError:
            return False
        else:
            if photos_num <= 10:
                bot.send_message(message.from_user.id, f'Загружаю по {message.text} фото.')
                hotels = get_hotels(message)
                for hotel_id, hotel_info in hotels.items():
                    photos = get_photos(hotel_id, photos_num)
                    if photos_num != 0:
                        for photo in photos:
                            bot.send_photo(message.from_user.id, photo)
                    bot.send_message(message.from_user.id, hotel_info)
                bot.send_message(message.from_user.id, 'Так же вы можете посмотреть:'
                                                       '\n/lowprice - дешёвые отели'
                                                       '\n/highprice - дорогие отели'
                                                       '\n/bestdeal - лучшее предложение'
                                                       '\n/history - история запросов')
            return True


if __name__ == '__main__':
    main()
