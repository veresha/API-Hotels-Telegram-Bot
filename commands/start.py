from telebot.types import Message
from load_bot import bot


@bot.message_handler(commands=['start', 'hello_world'])
def hello_message(message: Message) -> None:
    """Функция хендлер для команды /start"""
    bot.send_message(
        message.from_user.id,
        f'Привет, {message.from_user.username}! В какой ценовой категории будем искать отели?'
        '\n/lowprice - дешёвые отели, \n/highprice - дорогие отели, \n/bestdeal - лучшее предложение')
