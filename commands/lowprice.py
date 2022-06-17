from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
from getting_information import getting_information
import json


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    bot.send_message(message.from_user.id, "Дешёвые отели.")

    with open('user_info.json') as user_info_file:
        user_info = json.load(user_info_file)
        # print(user_info['availability_of_information'])

    if not user_info['availability_of_information']:
        bot.send_message(message.from_user.id, "Введите город в который хотите отправиться.")
        bot.set_state(message.from_user.id, UserState.city, message.chat.id)
        getting_information.main()
    else:
        bot.send_message(message.from_user.id, "Информация уже собрана.")
