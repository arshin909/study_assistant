from psycopg2 import connect
from collections import namedtuple
from json import loads


with open('config.json', 'r') as f:
    config = loads(f.read())

db_connect = connect(dbname='study_assistant', user='postgres', password='postgres', host='localhost')

MAX_LEN_DEQUE = 100
COURSE_LIFE = 21

BOT_INFORMATION = """
Данный бот создан для записи студентов на курсы созданные предподователями.
Студенты смогут записатся на курс и получить актуальное домашнее задание.
Предподователи смогут создать свои курс, добавлять домашнее задание для определенных групп 
и отслеживать успеваемость и посещаемость студентов.
"""

NEW_STUDENT = """
Введите информацию о себе: 
Группа
Номер зачетки
ФИО

Например:
ЗИВТм-1-18
1234567
Иванов Иван Иванович
"""

NEW_TEACHER = """

"""

NEW_COURSE = """
Введите информецию о курсе.
Название, продолжительность, семестр
Мат анализ, 120, 1
Список семестров:
{semesters}

Если нужного семестра нет, тогда создайте новый.
Создание курса в новом семетсре:
Название, продолжительность, старт семестра
Например:
Мат анализ, 120, 2019-01-30
"""


BOTTOMS_STUD_TYPE = namedtuple('bottoms_student', 'list my settings point visits homework')
Bottoms_stud = BOTTOMS_STUD_TYPE('Список курсов', 'Мои курсы', 'Настройки', 'Оценки', 'Посещаемость', 'Домашка')

BOTTOMS_TEACHER_TYPE = namedtuple('bottoms_teacher', 'course lessons settings')
Bottoms_teacher = BOTTOMS_TEACHER_TYPE('Курс', 'Занятия', 'Настройка')

BOTTOMS_TEACHER_COURSE = namedtuple('bottoms_teacher_course', 'list my add_course del_course group_sing_up back')
Bottoms_course = BOTTOMS_TEACHER_COURSE('Список курсов', 'Мои курсы', 'Создать', "Удалить", "Записать группу на курс",
                                        "Назад")

BOTTOMS_TEACHER_LESSON = namedtuple('bottoms_teacher_lesson', 'add_state  add_homework download start back')
Bottoms_lesson = BOTTOMS_TEACHER_LESSON("Загрузить статистику", "Загрузить задание", "Скачать статистику",
                                        "Начать занятие", "Назад")

SECRET_COMMAND = 'del me now'
example_path = './Example/example.xlsx'