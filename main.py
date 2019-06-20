# coding: utf-8

import telebot
import requests
import psycopg2

import config
import admin
import user

bot = telebot.TeleBot(config.token)

con = psycopg2.connect(
  database="equisk_study_assistant", 
  user="equisk_study_assistant",
  password="ARGJD4VKmYgj3eZ",
  host="postgresql.equisk.myjino.ru",
  port="5432"
)
# сервер: postgresql.equisk.myjino.ru
# порт 5432
# база equisk_study_assistant
# логин equisk_study_assistant
# пароль ARGJD4VKmYgj3eZ

cur = con.cursor()

@bot.message_handler(command=['/start'])
def start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/Регистрация', '/Вход')
    bot.send_message(message.chat.id, 'Здравствуйте! Вы хотите зарегистрироваться или вы уже зарегистрированы?', reply_markup=user_markup)

#как установить права админа? Пока сделал только через пароль - admin

@bot.message_handler(command=['/Вход'])
def authorization(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/Преподаватель', '/Студент')
    bot.send_message(message.chat.id, 'Выберите один из пунктов:', reply_markup=user_markup)

@bot.message_handler(command=['/Регистрация'])
def ask_name(message):
    bot.send_message(message.chat.id, 'Введите имя:')
    msg = bot.send_message(message.chat.id, 'Имя сохранено')

    cur.execute("INSERT INTO STUDENTS (FIRST_NAME) VALUE (user.send_message())")
    cur.execute("INSERT INTO STUDENTS (PATRONYMIC) VALUE (message.chat.id)")
    con.commit()

    bot.register_next_step_handler(msg, ask_last_name)

def ask_last_name(message):
    bot.send_message(message.chat.id, 'Введите фамилию:')
    msg = bot.send_message(message.chat.id, 'Фамилия сохранена')

    cur.execute("INSERT INTO STUDENTS (LAST_NAME) VALUE (user.send_message())")
    con.commit()  

    bot.register_next_step_handler(msg, ask_number_document)

def ask_number_document(message):
    bot.send_message(message.chat.id, 'Введите номер зачетной книжки:')
    msg = bot.send_message(message.chat.id, 'Номер зачетки сохранен')

    cur.execute("INSERT INTO STUDENTS (GROUP_ID) VALUE (user.send_message())")
    con.commit()

    bot.register_next_step_handler(msg, user.question_course)


bot.polling(none_stop=True)
