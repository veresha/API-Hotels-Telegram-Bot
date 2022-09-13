from load_bot import bot
import commands
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter
from users_info_storage.users_info_storage import load_users_info, save_users_info
from dbworker.dbworker import create_table


if __name__ == '__main__':
    create_table()
    load_users_info()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
    save_users_info()
