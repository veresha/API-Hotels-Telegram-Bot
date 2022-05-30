from telebot.types import Message
from load_bot import bot
from states.user_state import UserState


@bot.message_handler(commands=['start'])
def hello_message(message: Message):
    bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    bot.send_message(
        message.from_user.id,
        "Привет, в какой город хотите отправиться?")


@bot.message_handler(state=UserState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Записал! Теперь введите дату:')
        bot.set_state(message.from_user.id, UserState.city, message.chat.id)

        with bot.retrieve_city(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text.lower()
    else:
        bot.send_message(message.from_user.id, 'В имени города не может быть цифр.')


@bot.message_handler(state=UserState.date)
def get_date(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Записал! Теперь выберете дату:')
        bot.set_state(message.from_user.id, UserState.date, message.chat.id)

        with bot.retrieve_date(message.from_user.id, message.chat.id) as data:
            data['date'] = message.text
    else:
        bot.send_message(message.from_user.id, 'В дате должны быть цифры.')


# Тут должны быть кнопки выбора стоимости

# @bot.message_handler(state=UserState.hotel_price)
# def get_hotel_price(message: Message) -> None:
#     bot.send_message(message.from_user.id, 'Записал! Теперь выберете стоимость:')
#     bot.set_state(message.from_user.id, UserState.hotel_price, message.chat.id)
