from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
from users_info_storage.users_info_storage import users_info_dict
from getting_info import getting_info


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    bot.send_message(message.from_user.id, "Вы выбрали дешёвые отели. В какой город отправляемся?")
    users_info_dict[message.from_user.id] = [{'hotels_price': 'PRICE_LOWEST_FIRST'}]
    bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    getting_info.main()
