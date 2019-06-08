# coding: utf-8

import telebot

bot = telebot.TeleBot(config.token)

#нужна кнопка возврата назад

@bot.message_handler(commands=['Преподаватель'])
def admin(message):
    msg = bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(msg, ask_password)

def ask_password(message):
    text = message.text.lower()
    if not text == "admin":
        msg = bot.send_message(message.chat.id, 'Пароль неправильный! Попробуйте еще раз:')
        bot.register_next_step_handler(msg, ask_password)
        return
    msg2 = bot.send_message(message.chat.id, 'Спасибо, пароль верный')
    bot.register_next_step_handler(msg2, ask_choice)

def ask_choice(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Создать курс')
    user_markup.row('Загрузить расписание', 'Загрузить задания')
    user_markup.row('Разослать материалы студентам')
    user_markup.row('Скачать список студентов', 'Загрузить журнал успеваемости')
    bot.send_message(message.chat.id, 'Выберите один из пунктов:', reply_markup=user_markup)

@bot.message_handler(command=['Создать курс'])
def course(message):
    msg = bot.send_message(message.chat.id, 'Введите название курса:')
    bot.register_next_step_handler(msg, ask_course_name)

def ask_course_name(message):

    # нужен код для сохранения названия курса в базе courses

@bot.message_handler(command=['Загрузить расписание'])
def time_lessons(message):
    msg = bot.send_message(message.chat.id, 'Загрузите файл с расписанием')
    bot.register_next_step_handler(msg, ask_time_lessons)

def ask_time_lessons(message):
    
    # нужен код для загрузки материалов в базу lessons

@bot.message_handler(command=['Загрузить задания'])
def time_lessons(message):
    msg = bot.send_message(message.chat.id, 'Загрузите файл с заданием')
    bot.register_next_step_handler(msg, ask_study_materials)

def ask_study_materials(message): 
    
    # нужен код для загрузки материалов в базу lessons-media_resources_rels

@bot.message_handler(command=['Разослать материалы студентам'])
def send_study_materials(message):

    #нужен код для рассылки

    ids = open('', 'r')
    for id in ids:
        bot.send_message(chat_id=id, text="")

@bot.message_handler(command=['Скачать список студентов'])
def list_students(message):

    #нужен код для скачивания файлов со списком студентов с базы students

@bot.message_handler(command=['Загрузить журнал успеваемости'])
def gradebook(message):
    msg = bot.send_message(message.chat.id, 'Загрузите файл с заданием')
    bot.register_next_step_handler(msg, ask_gradebook)

def ask_gradebook(message): 

    # нужен код для загрузки материалов в базу students