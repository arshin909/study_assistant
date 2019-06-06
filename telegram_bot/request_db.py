from telegram_bot.helpers import cache
from telegram_bot.config import db_connect, COURSE_LIFE


class Base:

    @property
    def sql(self):
        if not self.sql:
            raise TypeError('Переменная с запросом пустая')
        else:
            return self.sql

    @sql.setter
    def sql(self, value):
        self.sql = value

    def get(self):
        with db_connect.cursor() as cursor:
            cursor.execute(self.sql)
            result = cursor.fetchone()
        return result or None

    def all(self):
        with db_connect.cursor() as cursor:
            cursor.execute(self.sql)
            result = cursor.fetchall()
        return result or []

    def commit(self):
        with db_connect.cursor() as cursor:
            cursor.execute(self.sql)
            db_connect.commit()


class People(Base):

    table = None
    sql = None

    def __init__(self, _id=None):
        if _id is not None:
            self.data = cache(_id) or self.get_people(_id).get()
            cache(_id, self.data)

    def get_people(self, _id):
        """ Записан студетн или нет """
        self.sql = f"""
            SELECT * FROM {self.table}
            WHERE telegram_id = '{_id}' 
        """
        return self

    def del_people(self):
        self.sql = f"""
            DELETE FROM {self.table} WHERE id = {self.data[0]}; 
        """
        return self

    def get_course(self, cource):
        self.sql = f"""
            SELECT * FROM courses WHERE id = {cource}
        """
        return self

    def get_group(self, group):
        self.sql = f"""
            SELECT * FROM groups WHERE id = {group}
        """
        return self

    def all_course(self):
        self.sql = f"""
            SELECT 
                c.id, 
                c.name, 
                initcap(concat(t.last_name, ' ', left(t.first_name, 1), '. ', left(t.patronymic, 1), '.')),
                s.start_date
            FROM courses as c,
                 semesters as s,
                 teachers as t
            WHERE c.semester_id = s.id
              AND s.start_date + interval '{COURSE_LIFE}' >= date_trunc('day', now())
              AND c.author = t.id
            ORDER BY s.start_date, c.id
        """
        return self

    def update_people(self, _id, data):

        new_field = [f'{k}={v}' for k, v in data.items()]
        if new_field:
           self.sql = f"""
                UPDATE {self.table}
                SET {','.join(new_field)}
                WHERE id = {_id}
            """
        return self


class Student(People):
    _type = 1
    table = 'students'

    def __new_group(self, group):
        """Записать новую группу"""
        self.sql = f"""
            INSERT INTO groups(name) VALUES ('{group}')
            ON CONFLICT DO NOTHING 
        """
        return self

    def create_group(self, name):
        """Создать и вернкть новую группу"""
        self.__new_group(name).commit()
        self.sql = f"SELECT id FROM groups WHERE name = '{name}'"
        return self.get()

    def create(self, student: dict):
        student['group_id'] = self.create_group(student['group_id'])
        self.sql = """
            INSERT INTO students(group_id, first_name, last_name, patronymic, gradebook_identy, telegram_id)  
            VALUES ({group_id}, '{first_name}', '{last_name}', '{patronymic}', '{gradebook}', '{id}')
        """.format(**student)
        return self

    def course_student(self):
        self.sql = f"""
            SELECT 
                c.id, 
                c.name,                 
                initcap(concat(t.last_name, ' ', left(t.first_name, 1), '. ', left(t.patronymic, 1), '.')) as author
            FROM 
                courses as c, 
                teachers as t, 
                "group-cource_rels" as gc
            WHERE 
                c.id = gc.cource_id AND 
                gc.group_id = {self.data[1]} AND 
                c.author = t.id
        """
        return self

    def get_point_visible(self, course, point=False):
        if point:
            table = 'student_performance'
            field = 'points'
        else:
            table = 'student_visits'
            field = 'visited '

        self.sql = f"""
            SELECT 
                l.date_time,
                {field}
            FROM 
                {table} as t,
                lessons as l
            WHERE 
                l.id = t.lesson_id AND 
                l.cource_id = {course} AND
                t.student_id = {self.data[0]}
            ORDER BY l.date_time
        """
        return self


class Teacher(People):
    _type = 0
    table = 'teachers'

    def create(self, student: dict):
        self.sql = """
            INSERT INTO teachers(first_name, last_name, patronymic, telegram_id)  
            VALUES ('{first_name}', '{last_name}', '{patronymic}', '{id}')
        """.format(**student)
        return self
