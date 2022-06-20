from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
from getting_info import getting_info
import json


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    bot.send_message(message.from_user.id, "Дешёвые отели.")
    # if not user_info['availability_of_information']:
    #     bot.send_message(message.from_user.id, "Введите город в который хотите отправиться.")
    #     bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    #     getting_info.main()
    # else:
    #     bot.send_message(message.from_user.id, "Информация уже собрана.")
