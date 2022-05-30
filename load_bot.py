import telebot
from telebot.storage import StateMemoryStorage
from config_data.config import BOT_TOKEN


storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=storage)
