# -*- coding: utf-8 -*-

from telegram_bot.student_branch import *


BOT_INFORMATION = """
Данный бот создан для записи студентов на курсы созданные предподователями.
Студенты смогут записатся на курс и получить актуальное домашнее задание.
Предподователи смогут создать свои курс, добавлять домашнее задание для определенных групп 
и отслеживать успеваемость и посещаемость студентов.
"""


# Обработчик команд start и help
@bot.message_handler(commands=['start', 'help'])
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

bot.polling(none_stop=True, interval=0)







