from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    city = State()
    date = State()
    hotel_price = State()
    photoes = State()
