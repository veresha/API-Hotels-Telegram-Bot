import telebot


def main():
    bot = telebot.TeleBot('5397321909:AAEfy-DvXMZ82aO_nYB9zqNZlEhi-c1Awu4')

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text.lower() == "привет":
            bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Напиши привет")
        elif message.text == "/hello_world":
            bot.send_message(message.from_user.id, "Мир отвечает тебе - Здравствуй!")
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
