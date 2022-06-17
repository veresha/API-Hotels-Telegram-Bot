from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    city = State()
    arrival_date = State()
    date_of_departure = State()
    hotel_price = State()
    hotels_number = State()
    photos = State()
