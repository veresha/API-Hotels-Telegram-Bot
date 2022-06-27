from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    city = State()
    choice_district = State()
    check_in = State()
    check_out = State()
    hotels_num = State()
    photos = State()
