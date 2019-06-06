# -*- coding: utf-8 -*-

from telebot import TeleBot, apihelper
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from telegram_bot.config import TOKEN, PROXY, BOT_INFORMATION
from telegram_bot.request_db import Student, Teacher
from telegram_bot.helpers import format_data
from telegram_bot.viewer import registration, create_user


# Запуск бота
apihelper.proxy = PROXY
bot = TeleBot(TOKEN)


# Обработчик команд start и help
@bot.message_handler(commands=['start', 'help', 'settings'])
def get_message(message: Message):
    text_answer = BOT_INFORMATION
    bottoms = {}

    if '/start' in message.text:
        text_answer += """ Вы студент или предподаватель? """
        markup = ReplyKeyboardMarkup(row_width=1)
        itembtn1 = KeyboardButton('/student - Студент')
        itembtn2 = KeyboardButton('/teacher - Предподователь')
        markup.add(itembtn1, itembtn2)
        bottoms['reply_markup'] = markup
    bot.send_message(message.chat.id, text_answer, **bottoms)


@bot.message_handler(commands=['student', 'teacher'])
def registration_user(message: Message):
    """Проверка пользователя на аутендификацию"""
    return bot.send_message(message.chat.id, **registration(message))


@bot.message_handler(func=lambda x: x.reply_to_message)
def new_user(message: Message):
    message.return_text = create_user(message)
    return registration_user(message)



@bot.message_handler(func=lambda x: Student(x.from_user.id).data)
def course(message: Message):
    text = message.text.lower()
    obj = Student(message.from_user.id)
    answer = None
    print(text)
    if Bottoms_stud.list.lower() == text:
        try:
            data = obj.all_course().all()
        except ValueError as error:
            print(error)
            return return_error(message)

        answer = f'Список курсов:\n\n'
        answer += format_data('{0}) {1} ({2}).\nНачало {3}\n', *data)

    elif Bottoms_stud.my.lower() == text:
        try:
            data = obj.course_student().all()
        except ValueError as error:
            print(error)
            return return_error(message)

        answer = f"Что бы просмотреть оценки или посещаемость по курсу введите:\nОценки [номер курса]\n" + \
            f"Посещаемость [номер курса]\n\nСписок курсов на которые подписаннва ваша группа:\n"
        answer += format_data('{0}) {1} ({2})\n', *data)
    elif text == 'del me now':
        if Student(message.from_user.id).data:
            user = Student(message.from_user.id)
        else:
            user = Teacher(message.from_user.id)
        user.del_people().commit()

    if answer:
        return bot.send_message(message.chat.id, answer)

    text = text.split(' ')
    if len(text) == 2 and text[1].isdigit():
        data = None
        if Bottoms_stud.point.lower() == text[0]:
            data = obj.get_point_visible(int(text[1]), True).all()
            answer = 'успеваемость'

        elif Bottoms_stud.visits.lower() == text[0]:
            data = obj.get_point_visible(int(text[1]), False).all()
            answer = Bottoms_stud.visits.lower()

        if answer:
            answer = f"Ваша {answer}" + format_data('{0} - {1}', *data)
            return bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, "Попробуйте снова! Потом.")

# Student stop

# Teacher start



# Teacher stop

def return_error(message: Message):
    text = "Данное действие для вас запрещенно!!!"
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True, interval=0)







