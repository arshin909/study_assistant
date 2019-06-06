# -*- coding: utf-8 -*-
import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(command=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Вы хотите зарегистрироваться или вы уже зарегистрированы?')
    user_markup = telebot.types.ReplyKeyboardMarkup()
    user_markup.row('/Регистрация', '/Вход')




bot.polling(none_stop=True)
