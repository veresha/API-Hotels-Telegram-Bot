import telebot
from config import token2


bot = telebot.TeleBot(token2)


@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")


bot.polling(none_stop=True, interval=0)
