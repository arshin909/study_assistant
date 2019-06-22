# -*- coding: utf-8 -*-
from re import compile
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ForceReply, File
from telebot import TeleBot

from telegram_bot.request_db import Teacher, Student
from telegram_bot.config import (
    NEW_STUDENT, NEW_TEACHER, Bottoms_stud, SECRET_COMMAND, BOT_INFORMATION, Bottoms_teacher, Bottoms_course,
    Bottoms_lesson, NEW_COURSE, example_path
)
from telegram_bot.helpers import deque_work, format_data, MyException, format_group
from telegram_bot.documents import Attachment


def base_command(message):
    """ Обработка основных команд """
    kwargs = {'text': BOT_INFORMATION}

    if '/start' in message.text:
        kwargs['text'] += "Вы студент или предподаватель?"
        kwargs['reply_markup'] = ReplyKeyboardMarkup(row_width=1)
        kwargs['reply_markup'].add(KeyboardButton('Студент(/student)'), KeyboardButton('Предподователь(/teacher)'))
    return kwargs


def registration(message: Message):
    user = message.from_user.id
    status_text = str(getattr(message, 'return_text', 'Вы заходите первый раз!\n'))

    if '/student' in message.text:
        user_obj = Student
        text = status_text + NEW_STUDENT
        bottoms = Bottoms_stud
        name = [3, 2]
    else:
        user_obj = Teacher
        text = status_text + NEW_TEACHER
        bottoms = Bottoms_teacher
        name = [2, 1]

    user_data = user_obj(user).data
    if user_data:
        markup = ReplyKeyboardMarkup(row_width=1)
        markup.add(*map(KeyboardButton, bottoms))
        text = f'Привет {" ".join(user_data[i].capitalize() for i in name)}'
    else:
        deque_work(user, 'w', user_obj._type)
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
        raise MyException('Что то пошло не так. Ваших данных нет храниилище.\n')

    data = r.search(message.text)
    if not data:
        raise MyException('Вы велли некоректные данные. \n')

    fio = data.group('fio').split(' ')
    user_info = {
        'last_name': fio[0],
        'first_name': fio[1],
        'patronymic': fio[2],
        'id': message.from_user.id
    }

    if cache[1] == Student._type:
        try:
            gradebook = int(data.group('number'))
        except (ValueError, TypeError):
            raise MyException('Номер зачетки должен быть числом.\n')

        user_info.update({
            'group_id': format_group(data.group('group')),
            'gradebook': gradebook,
        })

    obj().create(user_info).commit()


class StudentViewer:

    def __init__(self, bot: TeleBot):
        self.bot = bot

    def control(self, message: Message):
        text = message.text.lower()
        obj = Student(message.from_user.id)
        answer = None

        if Bottoms_stud.list.lower() == text:
            answer = f'Список курсов:\n\n' + format_data('{0}) {1} ({2}).\nНачало {3}\n', *obj.all_course().all())
        elif Bottoms_stud.my.lower() == text:
            answer = f"Что бы просмотреть оценки или посещаемость по курсу введите:\nОценки [номер курса]\n"
            answer += f"Посещаемость [номер курса]\n\nСписок курсов на которые подписаннва ваша группа:\n"
            answer += format_data('{0}) {1} ({2})\n', *obj.course_student().all()) or "Пока список пуст!"
        elif text == SECRET_COMMAND:
            obj.del_people().commit()
            message.text = '/start'
            self.bot.send_message(message.chat.id, **base_command(message))

        text_command = []
        if ' ' in text:
            text_command = text.split(' ')

        if len(text_command) < 2 or not text_command[1].isdigit():
            answer['text'] = 'Вы ввели некоректные данные после пробела.  Или в вашем сообщении нехватает инфомерации.'

        elif Bottoms_stud.point.lower() == text[0]:
            data = obj.get_point_visible(int(text[1]), True).all()
            answer = f"Ваша успеваемость\n" + format_data('{0} - {1}', *data)
        elif Bottoms_stud.visits.lower() == text[0]:
            data = obj.get_point_visible(int(text[1]), False).all()
            answer = f"Ваша {Bottoms_stud.visits.lower()}" + format_data('{0} - {1}', *data)

        if not answer:
            answer = "Попробуйте снова!!!"

        return self.bot.send_message(message.chat.id, answer)


class TeacherViewer:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def control(self, message: Message):
        text = message.text.lower()
        obj = Teacher(message.from_user.id)
        answer = {}

        if Bottoms_teacher.course.lower() == text:
            answer['text'] = 'Курсы'
            answer['reply_markup'] = ReplyKeyboardMarkup(row_width=2)
            answer['reply_markup'].add(*map(KeyboardButton, Bottoms_course))
        elif Bottoms_teacher.lessons.lower() == text:
            answer['text'] = 'Занятия'
            answer['reply_markup'] = ReplyKeyboardMarkup(row_width=2)
            answer['reply_markup'].add(*map(KeyboardButton, Bottoms_lesson))
        elif Bottoms_teacher.settings.lower() == text:
            pass
        elif text == SECRET_COMMAND:
            obj.del_people().commit()
            message.text = '/start'
            return base_command(message)

        if not answer:
            return Course(self.bot).control(message)

        return self.bot.send_message(message.chat.id, **answer)


class Course:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.obj = None

    def add_course(self, message: Message):
        r1 = compile(r'^[ \n]*(?P<name>[\w\d ]+),[ \n]*(?P<duration>[\d]+),[\n ](?P<semester>[\d]+)[ \n]*$')
        r2 = compile(
            r'^[ \n]*(?P<name>[\w\d ]+),[ \n]*(?P<duration>[\d]+),[\n ](?P<semester>\d\d\d\d-\d\d-\d\d)[ \n]*$')

        data = r1.search(message.text)
        new = False
        if not data:
            data = r2.search(message.text)
            new = True

        if not data:
            return self.bot.send_message(message.chat.id, 'Не удалось распознать данные')

        course_info = {
            'name': data.group('name'),
            'duration': data.group('duration'),
            'semester': data.group('semester'),
            'new': new
        }
        try:
            self.obj.create_course(course_info).commit()
        except MyException as error:
            return self.bot.send_message(message.chat.id, error)
        except Exception:
            return self.bot.send_message(message.chat.id, "Не удалось создать курс.")

        message.text = Bottoms_course.my
        return self.control(message)

    def del_course(self, message: Message):
        r = compile(r'^[ \n]*(?P<id>[\d]+)[ \n]*$')
        data = r.search(message.text)

        if not data:
            return self.bot.send_message(message.chat.id, 'Не удалось распознать идентифиактор курса')

        try:
            self.obj.del_course(data.group('id'))
        except MyException as error:
            return self.bot.send_message(message.chat.id, error)
        except Exception:
            return self.bot.send_message(message.chat.id, "Не удалось удалить курс")

        message.text = Bottoms_course.my
        return self.control(message)

    def sing_up(self, message: Message):
        r = compile(r'^[ \n]*(?P<id>[\d]+) [ \n]*(?P<group>[\w\W]+)[ \n]*$')
        data = r.search(message.text)

        if not data:
            return self.bot.send_message(message.chat.id, 'Не удалось распознать идентифиактор курса')

        # try:
        self.obj.sing_up_course(data.group('id'), format_group(data.group('group'))).commit()
        # except MyException as error:
        #     return self.bot.send_message(message.chat.id, error)
        # except Exception:
        #     return self.bot.send_message(message.chat.id, "Не удалось записать группу на курс.")

        return self.bot.send_message(message.chat.id, 'Готово')

    def control(self, message: Message):
        text = message.text.lower()
        self.obj = Teacher(message.from_user.id)
        answer = {}

        if Bottoms_course.list.lower() == text:
            answer['text'] = 'Список курсов:\n\n' + format_data('{0}, {1} ({2}).\nНачало {3}\n',
                                                                *self.obj.all_course().all())
        elif Bottoms_course.my.lower() == text:
            answer['text'] = "Список курсов у которых вы являетесь автором:\n"
            answer['text'] += format_data('{0}) {1}, {2} ({3})\n{4}\n', *self.obj.my_course().all()) or 'Пока список пуст.'
        elif Bottoms_course.add_course.lower() == text:
            answer['text'] = NEW_COURSE.format(semesters=format_data('{0} - {1}', *self.obj.get_semesters().all()))
            self.bot.register_next_step_handler(message, self.add_course)
        elif Bottoms_course.del_course.lower() == text:
            answer['text'] = "Список ваших курсов:\n"
            my_course = format_data('{0}) {1}, {2} ({3})\n', *self.obj.my_course().all())
            if not my_course:
                answer['text'] += 'Пока список пуст.'
            else:
                answer['text'] += my_course + '\nВведите номер курса для удаления.'
            self.bot.register_next_step_handler(message, self.del_course)
        elif Bottoms_course.group_sing_up.lower() == text:
            answer['text'] = "Введите номер курса и название группы. Например:\n1 зивтм-1-19"
            self.bot.register_next_step_handler(message, self.sing_up)
        elif Bottoms_course.back.lower() == text:
            message.text = '/start'
            answer = registration(message)

        if not answer:
            return LessonViewer(self.bot).control(message)

        return self.bot.send_message(message.chat.id, **answer)


class LessonViewer:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.obj = None
        self.download_state = {}
        self.download_homework = {}

    def control(self, message):
        text = message.text.lower()
        answer = {}
        self.obj = Teacher(message.from_user.id)

        if Bottoms_lesson.download.lower() == text:
            answer['text'] = 'Введите номер курса и название группы. Например:\n1 зивтм-1-18'
            self.bot.register_next_step_handler(message, self.get_state_file)
        elif Bottoms_lesson.add_state.lower() == text:
            answer['text'] = 'Отправте файл для загрузки и ввелите номер курса'
            self.bot.send_document(message.chat.id, open(example_path, 'rb'))
            self.bot.register_next_step_handler(message, self.download_data)
        elif Bottoms_lesson.add_homework.lower() == text:
            answer['text'] = 'Загрузите файл с домашкой и отдельным сообщением введи номер курса и название группы'
            self.bot.register_next_step_handler(message, self.download_data_homework)
        elif Bottoms_lesson.start.lower() == text:
            pass
        elif Bottoms_lesson.back.lower() == text:
            message.text = '/start'
            answer = registration(message)
        else:
            answer['text'] = 'Вы ввели некрорректные данные!'
        return self.bot.send_message(message.chat.id, **answer)

    def get_state_file(self, message: Message):
        r = compile(r'^[ \n]*(?P<course>[\d]+) (?P<group>[\w\W]+)[ \n]*$')

        data = r.search(message.text)
        if not data:
            return self.bot.send_message(message.chat.id, 'Вы велли некоректные данные.')

        course = data.group('course')
        group = format_group(data.group('group'))
        file = Attachment(message.from_user.id).get_state(course, group)
        return self.bot.send_document(message.chat.id, file)

    def download_data(self, message: Message):

        if message.document:
            file = self.bot.get_file(message.document.file_id)
            self.download_state['file'] = self.bot.download_file(file.file_path)
        elif message.text:
            r = compile(r'^[ \n]*(?P<id>[\d]+)[ \n]*$')
            data = r.search(message.text)
            if data:
                self.download_state['course'] = data.group('id')
        elif message.text.lower() == 'stop':
            message.text = '/start'
            return self.bot.send_message(message.chat.id, **registration(message))

        if len(self.download_state) == 2:
            try:
                text = Attachment(message.from_user.id).write_state(self.download_state['file'],
                                                                    self.download_state['course'])
            except Exception as error:
                print(error)
                text = 'При загрузки данных произошла ошибка'

            if not text:
                text = 'Готово'

            return self.bot.send_message(message.chat.id, text)
        else:
            return self.bot.register_next_step_handler(message, self.download_data)

    def download_data_homework(self, message: Message):
        if message.document:
            file = self.bot.get_file(message.document.file_id)
            self.download_homework['file'] = self.bot.download_file(file.file_path)
        elif message.text:
            r = compile(r'^[ \n]*(?P<course>[\d]+) [ \n]*(?P<group>[\w\W]+)[ \n]*$')
            data = r.search(message.text)
            if data:
                self.download_homework['course'] = data.group('course')
                self.download_homework['group'] = data.group('group')


