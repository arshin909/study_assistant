# coding: utf-8

import telebot
import requests
import psycopg2

import config

con = psycopg2.connect(
  database="equisk_study_assistant", 
  user="equisk_study_assistant",
  password="ARGJD4VKmYgj3eZ",
  host="postgresql.equisk.myjino.ru",
  port="5432"
)

cur = con.cursor()

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['/Преподаватель'])
def ask_registration_admin(message):
    if not str(message.chat.id) == config.users:
        msg = bot.send_message(message.chat.id, 'Извините, у вас нет доступа')
    msg2 = bot.send_message(message.chat.id, 'Здравствуйте, ' + str(message.chat.username))
    bot.register_next_step_handler(msg2, ask_choice)

def ask_choice(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/Создать курс')
    user_markup.row('/Загрузить материалы')
    user_markup.row('/Разослать материалы студентам')
    user_markup.row('/Скачать список студентов', '/Загрузить журнал успеваемости')
    bot.send_message(message.chat.id, 'Выберите один из пунктов:', reply_markup=user_markup)

@bot.message_handler(command=['/Создать курс'])
def course(message):
    bot.send_message(message.chat.id, 'Введите название курса:')

    cur.execute("INSERT INTO COURSES (NAME) VALUE (user.send_message())")
    con.commit() 

    bot.send_message(message.chat.id, 'Название сохранено')
    
@bot.message_handler(command=['/Загрузить материалы'])
def send_materials(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/Загрузить расписание')
    user_markup.row('/Загрузить задания')
    user_markup.row('/Загрузить учебные пособия')
    bot.send_message(message.chat.id, 'Выберите один из пунктов:', reply_markup=user_markup)

@bot.message_handler(command=['/Загрузить расписание'])
def time_lessons(message):
    msg = bot.send_message(message.chat.id, 'Загрузите файл')
    bot.register_next_step_handler(msg, ask_time_lessons)
    
def ask_time_lessons(message):
    try:
        file_info_link = f'https://api.telegram.org/bot{config.token}/getFile?file_id={file_id}'
        file_path = requests.get(file_info_link).json()['result']['file_path']
        file_link = f'https://api.telegram.org/file/bot{config.token}/{file_path}'
        file = requests.get(file_link).content

        cur.execute("INSERT INTO LESSONS (DATE_TIME) VALUE (file_info)")
        cur.execute("INSERT INTO TG_FILE_STORAGE (PATH) VALUE (file)")
        con.commit()

        bot.reply_to(message,"Файл добавлен") 
   
    except Exception as e:
        bot.reply_to(message,e)

@bot.message_handler(command=['/Загрузить задания'])
def time_lessons(message):
    msg = bot.send_message(message.chat.id, 'Загрузите файл')
    bot.register_next_step_handler(msg, ask_study_materials)

def ask_study_materials(message): 
    try:
        file_info_link = f'https://api.telegram.org/bot{config.token}/getFile?file_id={file_id}'
        file_path = requests.get(file_info_link).json()['result']['file_path']
        file_link = f'https://api.telegram.org/file/bot{config.token}/{file_path}'
        file = requests.get(file_link).content

        cur.execute("INSERT INTO LESSON-MEDIA_RESOURCE_RELS (MEDIA_RESOURCE_ID) VALUE (file_info)")
        cur.execute("INSERT INTO TG_FILE_STORAGE (PATH) VALUE (file)")
        con.commit()

        bot.reply_to(message,"Файл добавлен") 
   
    except Exception as e:
        bot.reply_to(message,e)
        
@bot.message_handler(command=['/Загрузить учебные пособия'])
def time_lessons(message):
    msg = bot.send_message(message.chat.id, 'Загрузите файл')
    bot.register_next_step_handler(msg, ask_tutorial)
    
def ask_tutorial(message): 
    try:
        file_info_link = f'https://api.telegram.org/bot{config.token}/getFile?file_id={file_id}'
        file_path = requests.get(file_info_link).json()['result']['file_path']
        file_link = f'https://api.telegram.org/file/bot{config.token}/{file_path}'
        file = requests.get(file_link).content

        cur.execute("INSERT INTO MEDIA_RESOURCES (NAME) VALUE (file_info)")
        cur.execute("INSERT INTO TG_FILE_STORAGE (PATH) VALUE (file)")
        con.commit()

        bot.reply_to(message,"Файл добавлен") 
   
    except Exception as e:
        bot.reply_to(message,e)
        
@bot.message_handler(command=['/Разослать материалы студентам'])
def send_choice(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/Разослать расписание')
    user_markup.row('/Разослать задания')
    user_markup.row('/Разослать учебные пособия')
    bot.send_message(message.chat.id, 'Выберите один из пунктов:', reply_markup=user_markup)

@bot.message_handler(command=['/Разослать расписание'])
def send_time_lessons(message):
    bot.send_message(message.chat.id, 'Выберите файл')

    cur.execute("SELECT DATE_TIME from LESSONS")
    cur.execute("SELECT PATH from TG_FILE_STORAGE")

    rows = cur.fetchall()
    for r in rows:  
        print("НАЗВАНИЕ =", r[0])
        print("ФАЙЛ =", r[1], "\n")

        # код рассылки

@bot.message_handler(command=['/Разослать задания'])
def send_study_materials(message):
    bot.send_message(message.chat.id, 'Выберите файл')

    cur.execute("SELECT MEDIA_RESOURCE_ID_TIME from LESSON-MEDIA_RESOURCE_RELS")
    cur.execute("SELECT PATH from TG_FILE_STORAGE")

    rows = cur.fetchall()
    for r in rows:  
        print("НАЗВАНИЕ =", r[0])
        print("ФАЙЛ =", r[1], "\n")
            
        # код рассылки    
            
@bot.message_handler(command=['/Разослать учебные пособия'])
def send_tutorial(message):
    bot.send_message(message.chat.id, 'Выберите файл')

    cur.execute("SELECT NAME from MEDIA_RESOURCES")
    cur.execute("SELECT PATH from TG_FILE_STORAGE")

    rows = cur.fetchall()
    for r in rows:  
        print("НАЗВАНИЕ =", r[0])
        print("ФАЙЛ =", r[1], "\n")
    
    # cur.execute("SELECT PATRONYMIC from STUDENTS")
    # for i in PATRONYMIC:

    # doc = open('/tmp/file.txt', 'rb')
    # bot.send_document(message.chat.id, doc)
    # bot.send_document(message.chat.id, "FILEID")

@bot.message_handler(command=['/Скачать список студентов'])
def list_students(message):
    bot.send_message(message.chat.id, 'Выберите файл')

    cur.execute("SELECT FIRST_NAME, LAST_NAME, GROUP_ID, GRADEBOOK_IDENTY from STUDENTS")

    rows = cur.fetchall()
    for r in rows:  
        print("НАЗВАНИЕ =", r[0])
        print("ФАЙЛ =", r[1])
        print("НОМЕР ЗАЧЕТКИ =", r[2])
        print("УСПЕВАЕМОСТЬ =", r[3], "\n")

        # нужен код для скачивания файлов со списком студентов с таблицы students


@bot.message_handler(command=['/Загрузить журнал успеваемости'])
def gradebook(message):
    msg = bot.send_message(message.chat.id, 'Загрузите файл с заданием')
    bot.register_next_step_handler(msg, ask_gradebook)

def ask_gradebook(message): 
    try:
        file_info_link = f'https://api.telegram.org/bot{config.token}/getFile?file_id={file_id}'
        file_path = requests.get(file_info_link).json()['result']['file_path']
        file_link = f'https://api.telegram.org/file/bot{config.token}/{file_path}'
        file = requests.get(file_link).content

        cur.execute("INSERT INTO STUDENTS (GRADEBOOK_IDENTY) VALUE (file_info)")
        cur.execute("INSERT INTO TG_FILE_STORAGE (PATH) VALUE (file)")
        con.commit()

        bot.reply_to(message,"Файл добавлен") 
   
    except Exception as e:
        bot.reply_to(message,e)
