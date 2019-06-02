""" Создание бота """

from telebot import TeleBot, apihelper
from telegram_bot.config import TOKEN, PROXY

# Запуск бота
apihelper.proxy = PROXY
bot = TeleBot(TOKEN)
