from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    city = State()
    check_in = State()
    check_out = State()
    hotels_num = State()
    choice_district = State()
    photos = State()
    work_with_api = State()
