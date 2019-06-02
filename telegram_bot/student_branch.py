import re

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ForceReply
from collections import namedtuple

from telegram_bot.student import Student
from telegram_bot.helpers import deque_work
from telegram_bot.connect import bot


NEW_STUDENT = """
Вы заходите первый раз! Введите информацию о себе: 
Группа
Номер зачетки
ФИО

Например:
ЗИВТм-1-18
1234567
Иванов Иван Иванович
"""

BOTTOMS_TYPE = namedtuple('bottoms', 'list my settings subscribe unsubscribe point')
Bottoms = BOTTOMS_TYPE('Список курсов', 'Мои курсы', 'Настройки', 'Записаться', 'Отписаться', 'Оценки')


@bot.message_handler(commands=['student'])
def student(message: Message):
    stud = Student()
    if not stud.get_people(message):
        write_student_data(message)
    else:
        student_allow(message)


def write_student_data(message: Message):
    deque_work(message.from_user.id, Student.type_)
    markup = ForceReply(selective=False)
    bot.send_message(message.chat.id, NEW_STUDENT, reply_markup=markup)


@bot.message_handler(func=lambda x: x.reply_to_message)
def new_student(message: Message):
    if not deque_work(message.reply_to_message.chat.id):
        bot.send_message(message.chat.id, "Попробуйте снова! Потом.")

    text = message.text
    r = re.compile(r'^[ \n]*(?P<group>[\w\W]+)\n(?P<number>[\d]+)\n(?P<fio>[\w]+ [\w]+ [\w]+)[ \n]*$')
    student_data = r.search(text)
    if not student_data:
        return student(message)

    (message.from_user.last_name, message.from_user.first_name, message.from_user.patronymic) = \
        student_data.group('fio').split(' ')
    message.from_user.group_id = str(student_data.group('group')).lower().replace(' ', '')

    try:
        message.from_user.gradebook = int(student_data.group('number'))
    except (ValueError, TypeError):
        return student(message)

    Student().create_student(message)


def student_allow(message: Message):
    markup = ReplyKeyboardMarkup(row_width=1)
    itembtn1 = KeyboardButton(Bottoms.list)
    itembtn2 = KeyboardButton(Bottoms.my)
    itembtn3 = KeyboardButton(Bottoms.settings)
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, 'Курсы:', reply_markup=markup)


@bot.message_handler()
def course(message: Message):
    print(message.text)
    if Bottoms.list == message.text:
        _list = Student().cource_list()
        print(_list)
