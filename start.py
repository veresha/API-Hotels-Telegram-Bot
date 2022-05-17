from load_bot import bot


@bot.message_handler(commands=['/start'])
def hello_message(message):
    bot.send_message(message.chat.id, "Привет, чем я могу тебе помочь?")


def main():
    hello_message()  # Какой именно аргумент тут надо передавать и надо ли вообще


if __name__ == '__main__':
    main()
