from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    city = State()
    check_in = State()
    check_out = State()
    hotel_price = State()
    hotels_number = State()
    photos = State()
