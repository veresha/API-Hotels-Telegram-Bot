from load_bot import bot


@bot.message_handler(commands=['/help'])
def help_message(message):
    bot.send_message(message.chat.id, "Напиши /start")


def main():
    help_message()  # Какой именно аргумент тут надо передавать и надо ли вообще


if __name__ == '__main__':
    main()
