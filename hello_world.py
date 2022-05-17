from load_bot import bot


@bot.message_handler(commands=['hello_world'])
def hello_world_message(message):
    bot.send_message(message.chat.id, "Мир отвечает тебе - Здравствуй!")


def main():
    hello_world_message()


if __name__ == '__main__':
    main()


