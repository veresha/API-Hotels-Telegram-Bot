from telebot.types import Message
from load_bot import bot


@bot.message_handler(commands=['help'])
def help_message(message: Message) -> None:
    """Функция-хэндлер для команды /help"""
    bot.send_message(message.from_user.id, "Список команд:"
                                           "\n/start - начать"
                                           "\n/lowprice - дешёвые отели"
                                           "\n/highprice - дорогие отели"
                                           "\n/bestdeal - лучшее предложение"
                                           "\n/history - история запросов")
