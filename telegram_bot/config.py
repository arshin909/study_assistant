from psycopg2 import connect
from collections import namedtuple


BOT_NAME = 'StudyAssistantBot'

TOKEN = '827818439:AAH7W0UVu6CMgBTjyKq9tAWzwUT2NgXEivA'

Login = 'KgeuStudyAssistantBot'

PROXY = {
    'http': 'http://84.22.98.104:52001',
    'https': 'socks5://blackm:city17@84.22.98.104:52003'
}

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

BOTTOMS_STUD_TYPE = namedtuple('bottoms', 'list my settings point visits')
Bottoms_stud = BOTTOMS_STUD_TYPE('Список курсов', 'Мои курсы', 'Настройки', 'Оценки', 'Посещаемость')

BOTTOMS_TEATCHER_TYPE = namedtuple('bottoms', 'list my settings point visits')
Bottoms_teacher = BOTTOMS_TEATCHER_TYPE('Список курсов', 'Мои курсы', 'Настройки', 'Оценки', 'Посещаемость')
