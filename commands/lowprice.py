from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
from getting_info import getting_info
from users_info_storage.users_info_storage import users_info_dict


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    bot.send_message(message.from_user.id, "Вы выбрали дешёвые отели.")
    users_info_dict[getting_info.new_user_id] += [{'hotels_price': 'PRICE_LOWEST_FIRST'}]
    bot.set_state(message.from_user.id, UserState.hotels_num, message.chat.id)
