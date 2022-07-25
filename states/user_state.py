from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    city = State()
    choice_district = State()
    check_in = State()
    check_out = State()
    min_price = State()
    max_price = State()
    min_dist = State()
    max_dist = State()
    hotels_num = State()
    photos_num = State()
