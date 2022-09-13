from telebot.types import Message
from load_bot import bot
from dbworker.dbworker import get_history


@bot.message_handler(commands=['history'])
def history(message: Message):
    bot.send_message(message.from_user.id, "История запросов:")
    users_history = get_history(message.from_user.id)
    print(users_history[0])
    for i in users_history:
        if i[8] or i[9] is None:
            min_price = 'не указана'
            max_price = 'не указана'
        else:
            min_price = i[8] + '$'
            max_price = i[9] + '$'
        info = f'ID_пользователя: {i[0]}\n' \
               f'Дата запроса: {i[1]}\n' \
               f'Команда: {i[2]}\n' \
               f'Город/район: {i[3]}\n' \
               f'Количество отелей: {i[5]}\n' \
               f'Название отеля: {i[4]}\n' \
               f'Дата заезда: {i[6]}\n' \
               f'Дата выезда: {i[7]}\n' \
               f'Минимальная цена: {min_price}\n' \
               f'Максимальная цена: {max_price}\n' \
               f'Сайт отеля: {i[10]}\n' \
               f'Расстояние до центра: {i[11]}\n' \
               f'Стоимость за весь период: {i[12]}$'
        bot.send_message(message.from_user.id, info)
    bot.send_message(message.from_user.id, 'Желаете выполнить ещё какое-то действие?\n/lowprice - дешёвые отели,'
                                           '\n/highprice - дорогие отели,\n/bestdeal - лучшее предложение')

