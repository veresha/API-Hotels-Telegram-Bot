import telebot
from config import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, "Напиши привет")


def main():
    # вот тут проблемка

    help_message(message)


if __name__ == '__main__':
    main()
