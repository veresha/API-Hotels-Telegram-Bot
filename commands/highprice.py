from telebot.types import Message
from load_bot import bot


@bot.message_handler(commands=['highprice'])
def hello_world_message(message: Message):
    bot.send_message(message.from_user.id, "Дорогие отели.")