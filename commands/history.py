from telebot.types import Message
from load_bot import bot
from dbworker.dbworker import get_history


@bot.message_handler(commands=['history'])
def hello_world_message(message: Message):
    bot.send_message(message.from_user.id, "История запросов:")
    users_history = get_history(message.from_user.id)
    print(users_history[0])
    for i in users_history:
        info = f'ID_пользователя: {i[0]}\n' \
               f'Дата запроса: {i[1]}\n' \
               f'Команда: {i[2]}\n' \
               f'Город/район: {i[3]}\n' \
               f'Количество отелей: {i[4]}\n' \
               f'Дата заезда: {i[5]}\n' \
               f'Дата выезда: {i[6]}\n' \
               f'Минимальная цена: {i[7]}\n' \
               f'Максимальная цена: {i[8]}\n' \
               f'Сайт отеля: {i[9]}\n' \
               f'Расстояние до центра: {i[10]}\n' \
               f'Стоимость за весь период: {i[11]}$'
        bot.send_message(message.from_user.id, info)
    bot.send_message(message.from_user.id, 'Желаете выполнить ещё какое-то действие?\n/lowprice - дешёвые отели,'
                                           '\n/highprice - дорогие отели,\n/bestdeal - лучшее предложение')

