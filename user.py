# coding: utf-8

import telebot 
# coding: utf-8

import telebot

bot = telebot.TeleBot(config.token)

#нужна кнопка возврата назад

@bot.message_handler(commands=['Студент'])
def registration_course(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('#указать имя курса из базы courses')
    bot.send_message(message.chat.id, 'На какой курс вы хотите записаться?', reply_markup=user_markup)

@bot.message_handler(command=['#указать имя курса из базы courses'])
def ask_choice_user(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Получить расписание', 'Получить задания')
    bot.send_message(message.chat.id, 'Выберите один из пунктов:', reply_markup=user_markup)

@bot.message_handler(command=['Получить расписание'])
def take_time_lessons(message):
        
        #нужен код для скачивания расписания с базы lessons

@bot.message_handler(command=['Получить задания'])
def take_study_materials(message):
        
        #нужен код для скачивания файлов с базы lessons-media_resources_rels
