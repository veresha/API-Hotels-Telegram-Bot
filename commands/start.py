from telebot.types import Message
from load_bot import bot
from states.user_state import UserState
from getting_information import getting_information


@bot.message_handler(commands=['start'])
def hello_message(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.city, message.chat.id)
    bot.send_message(
        message.from_user.id,
        "Привет, в какой город хотите отправиться?"
    )


getting_information.main()
