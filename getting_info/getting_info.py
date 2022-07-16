from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
import functools
from users_info_storage.users_info_storage import users_info_dict
from work_with_api.work_with_api import get_city_districts, get_hotels, get_photos
from telebot.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from keyboards.reply.district_choice import district_choice
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import datetime
from loguru import logger


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
        calendar, step = DetailedTelegramCalendar(locale='ru', min_date=datetime.date.today()).build()
        bot.send_message(message.from_user.id, f'Теперь выберете дату заселения',
                         reply_markup=calendar)

        @bot.callback_query_handler(state=UserState.check_in, func=DetailedTelegramCalendar.func())
        def callback_check_in(callback):
            result, key, step = DetailedTelegramCalendar(
                locale='ru', min_date=datetime.date.today()).process(callback.data)
            if not result and key:
                bot.edit_message_text(f"Выберите {LSTEP[step]}",
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
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(message.from_user.id, f'Теперь выберете дату выезда',
                         reply_markup=calendar)
        check_in_date = datetime.datetime.strptime(
            users_info_dict[message.from_user.id][3]['check_in'], "%Y-%m-%d").date()

        @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
        def callback_check_out(callback):
            result, key, step = DetailedTelegramCalendar(
                locale='ru', min_date=check_in_date).process(callback.data)
            if not result and key:
                bot.edit_message_text(f"Выберите {LSTEP[step]}",
                                      callback.message.chat.id,
                                      callback.message.message_id,
                                      reply_markup=key)
            elif result:
                bot.edit_message_text(f"Записал! Дата выезда {result}.\nСколько отелей показать?",
                                      callback.message.chat.id,
                                      callback.message.message_id)
                users_info_dict[message.from_user.id].append({'check_out': str(result)})
                bot.set_state(message.from_user.id, UserState.hotels_num, message.chat.id)

    @decorator_check_info('Ошибка ввода, это должна быть цифра!')
    @bot.message_handler(state=UserState.hotels_num)
    def get_hotels_num(message: Message) -> bool:
        try:
            hotels_num = int(message.text)
        except ValueError:
            return False
        else:
            logger.debug('Запрос у пользователя кол-ва фоток')
            bot.send_message(message.from_user.id, f'Записал, выводим {hotels_num} отеля/ей.\n'
                                                   f'Сколько фото каждого отеля нужно?')
            hotels = get_hotels(message, hotels_num)
            users_info_dict[message.from_user.id].append({'hotels': hotels})
            bot.set_state(message.from_user.id, UserState.photos_num, message.chat.id)
            logger.debug('Состояние сменилось')
            return True

    @decorator_check_info('Ошибка ввода, это должна быть цифра!')
    @bot.message_handler(state=UserState.photos_num)
    def get_photos_num(message: Message) -> bool:
        logger.debug('Запрос кол-ва фоток прошёл')
        try:
            photos_num = int(message.text)
        except ValueError:
            return False
        else:
            bot.send_message(message.from_user.id, f'Загружаю {message.text} фото')
            for hotel_id, hotel_info in users_info_dict[message.from_user.id][5]['hotels'].items():
                # photos = get_photos(hotel_id, photos_num)
                # for photo in photos:
                #     bot.send_photo(message.from_user.id, photo)
                bot.send_message(message.from_user.id, hotel_info)
            return True


if __name__ == '__main__':
    main()
