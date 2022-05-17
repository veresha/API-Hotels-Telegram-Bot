import telebot
from config import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['hello_world'])
def hello_world_message(message):
    bot.send_message(message.from_user.id, "Мир отвечает тебе - Здравствуй!")


def main():
    # вот тут проблемка

    hello_world_message(message)


if __name__ == '__main__':
    main()


