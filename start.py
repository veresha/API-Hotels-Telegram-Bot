import telebot
from config import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['/start'])
def hello_message(message):
    bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")


def main():
    # вот тут проблемка

    hello_world_message(message)


if __name__ == '__main__':
    main()