# coding: utf-8

import telebot
import config
import psycopg2

bot = telebot.TeleBot(config.token)

con = psycopg2.connect(
  database="equisk_study_assistant", 
  user="equisk_study_assistant",
  password="ARGJD4VKmYgj3eZ",
  host="postgresql.equisk.myjino.ru",
  port="5432"
)
    
cur = con.cursor()

@bot.message_handler(commands=['/Студент'])
def question_course(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/Получить расписание', '/Получить задания')
    bot.send_message(message.chat.id, 'Выберите один из пунктов:', reply_markup=user_markup)

@bot.message_handler(command=['/Получить расписание'])
def take_time_lessons(message):
    bot.send_message(message.chat.id, 'Выберите файл')

    cur.execute("SELECT DATE_TIME from LESSONS")
    cur.execute("SELECT PATH from TG_FILE_STORAGE")

    rows = cur.fetchall()
    for r in rows:  
        print("НАЗВАНИЕ =", r[0])
        print("ФАЙЛ =", r[1], "\n")

@bot.message_handler(command=['/Получить задания'])
def take_study_materials(message):
    bot.send_message(message.chat.id, 'Выберите файл')

    cur.execute("SELECT MEDIA_RESOURCE_ID_TIME from LESSON-MEDIA_RESOURCE_RELS")
    cur.execute("SELECT PATH from TG_FILE_STORAGE")

    rows = cur.fetchall()
    for r in rows:  
        print("НАЗВАНИЕ =", r[0])
        print("ФАЙЛ =", r[1], "\n")
