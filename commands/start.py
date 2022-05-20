from telebot.types import Message
from load_bot import bot


@bot.message_handler(commands=['start'])
def hello_message(message: Message):
    bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
