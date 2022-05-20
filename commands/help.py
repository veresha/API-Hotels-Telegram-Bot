from telebot.types import Message
from load_bot import bot


# /help -> help
@bot.message_handler(commands=['help'])
def help_message(message: Message):
    bot.send_message(message.from_user.id, "Напиши /start")
