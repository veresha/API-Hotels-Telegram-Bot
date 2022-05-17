import telebot
from config import token
# Вопрос по поводу того, что если импортировать весь файл(как понимаю именно так надо), то как запустить функцию?
# Ведь в файлах питон не знает, что за message такой
from help import help_message
from hello_world import hello_world_message
from start import hello_message


def main():
    bot = telebot.TeleBot(token)

    # Если убрать скрипт ниже, то как сделать, чтобы подключённые модули запустились?
    # Всю инфу по ботам что нашёл - везде все объясняют только создание ботов в один файл

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text.lower() == "привет" or '/start':
            hello_message(message)
        elif message.text == "/hello_world":
            hello_world_message(message)
        elif message.text == '/help':
            help_message(message)
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
