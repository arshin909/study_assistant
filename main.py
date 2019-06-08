# coding: utf-8

import telebot
import config
import admin
import user
import logging as log

bot = telebot.TeleBot(config.token)

@bot.message_handler(command=['start'])
def start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Регистрация', 'Вход')
    bot.send_message(message.chat.id, 'Здравствуйте! Вы хотите зарегистрироваться или вы уже зарегистрированы?', reply_markup=user_markup)

#как установить права админа?
@bot.message_handler(command=['Вход'])
def authorization(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Преподаватель', 'Студент')
    bot.send_message(message.chat.id, 'Выберите один из пунктов:', reply_markup=user_markup)

@bot.message_handler(command=['Регистрация'])
def registration(message):
    bot.send_message(message.chat.id, 'Укажите для регистрации адрес электронной почты')

# регистрация


@bot.message_handler(command=['settings'])
def registration(message):
    bot.send_message(message.chat.id, 'Укажите для регистрации адрес электронной почты')



@bot.message_handler(command=['help'])
def registration(message):
    bot.send_message(message.chat.id, 'Укажите для регистрации адрес электронной почты')




bot.polling(none_stop=True)
