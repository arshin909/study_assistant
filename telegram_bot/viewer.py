# -*- coding: utf-8 -*-
from re import compile
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ForceReply

from telegram_bot.request_db import Teacher, Student
from telegram_bot.config import NEW_STUDENT, NEW_TEACHER, Bottoms_stud, Bottoms_teacher
from telegram_bot.helpers import deque_work


def registration(message: Message):
    user = message.from_user.id
    status_text = getattr(message, 'return_text', 'Вы заходите первый раз!\n')

    if '/student' in message.text:
        user_obj = Student
        text = status_text + NEW_STUDENT
        bottoms = Bottoms_stud
    else:
        user_obj = Teacher
        text = status_text + NEW_TEACHER
        bottoms = Bottoms_teacher

    user_data = user_obj(user).data
    if user_data:
        markup = ReplyKeyboardMarkup(row_width=1)
        markup.add(*map(KeyboardButton, bottoms))
        text = f'Привет {user_data[3].capitalize()} {user_data[2].capitalize()}'
    else:
        deque_work(user, user_obj._type, 'w')
        markup = ForceReply(selective=False)

    return {'text': text, 'reply_markup': markup}


def create_user(message: Message):
    cache = deque_work(message.reply_to_message.chat.id, 'r')
    if cache and cache[1] == Student._type:
        r = compile(r'^[ \n]*(?P<group>[\w\W]+)\n(?P<number>[\d]+)\n(?P<fio>[\w]+ [\w]+ [\w]+)[ \n]*$')
        obj = Student
    elif cache and cache[1] == Teacher._type:
        r = compile(r'^[ \n]*(?P<fio>[\w]+ [\w]+ [\w]+)[ \n]*$')
        obj = Teacher
    else:
        return 'Что то пошло не так. Ваших данных нет храниилище.\n'

    student_data = r.search(message.text)
    if student_data:
        return 'Вы велли некоректные данные. \n'

    fio = student_data.group('fio').split(' ')
    user_info = {
        'last_name': fio[0],
        'first_name': fio[1],
        'patronymic': fio[2],
        'id': message.from_user.id
    }

    if cache[1] == Student._type:
        try:
            gradebook = int(student_data.group('number'))
        except (ValueError, TypeError):
            return 'Номер зачетки должен быть числом.\n'
        user_info.update({
            'group_id': str(student_data.group('group')).lower().replace(' ', ''),
            'gradebook': gradebook,
        })

    obj().create(user_info).commit()
