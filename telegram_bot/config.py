from psycopg2 import connect


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