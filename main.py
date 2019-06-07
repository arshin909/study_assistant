# -*- coding: utf-8 -*-
import config
import telebot

bot = telebot.TeleBot(config.token)

@bot.message_handler(command=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/Регистрация', '/Вход')
    bot.send_message(message.from_user.id, 'Здравствуйте! Вы хотите зарегистрироваться или вы уже зарегистрированы?', reply_markup=user_markup)





bot.polling(none_stop=True)
