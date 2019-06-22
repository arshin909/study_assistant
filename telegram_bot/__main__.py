# -*- coding: utf-8 -*-

from telebot import TeleBot, apihelper
from telebot.types import Message, ForceReply

from telegram_bot.config import config
from telegram_bot.request_db import Student, Teacher
from telegram_bot.viewer import (
    registration, create_user, StudentViewer, TeacherViewer, MyException, base_command
)


# Запуск бота
apihelper.proxy = config.get('proxy')
bot = TeleBot(config.get('token'))


# Обработчик команд start и help
@bot.message_handler(commands=['start', 'help', 'settings'])
def get_message(message: Message):
    result = base_command(message)
    return bot.send_message(message.chat.id, **result)


@bot.message_handler(content_types=['document'])
def get_document(message: Message):
    print(message.document)


@bot.message_handler(func=lambda x: '/student' in x.text or '/teacher' in x.text, content_types=['text'])
def registration_user(message: Message):
    """Проверка пользователя на аутендификацию"""
    result = registration(message)
    if type(result.get('reply_markup')) == ForceReply:
        bot.register_next_step_handler(message, new_user)
    return bot.send_message(message.chat.id, **result)


def new_user(message: Message):
    try:
        create_user(message)
    except MyException as error:
        message.return_text = error
    return registration_user(message)


@bot.message_handler(func=lambda x: Student(x.from_user.id).data)
def is_student(message: Message):
    return StudentViewer(bot).control(message)


@bot.message_handler(func=lambda x: Teacher(x.from_user.id).data)
def is_teacher(message: Message):
    return TeacherViewer(bot).control(message)


bot.polling(none_stop=True, interval=0)





