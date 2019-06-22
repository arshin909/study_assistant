from telegram_bot.helpers import cache, MyException
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

    def commit_return(self):
        with db_connect.cursor() as cursor:
            cursor.execute(self.sql)
            result = cursor.fetchone()
            db_connect.commit()
        return result

    def commit_returns(self):
        with db_connect.cursor() as cursor:
            cursor.execute(self.sql)
            result = cursor.fetchall()
            db_connect.commit()
        return result


class People(Base):

    table = None
    sql = None
    _type = None

    def __init__(self, _id=None):
        if _id is None:
            return

        data = cache(_id)
        if data and data[0] == self._type:
            self.data = data[1]
        else:
            self.data = self.get_people(_id).get()

        cache(_id, (self._type, self.data))

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

    def get_group(self, _id=None, name=None):
        if _id or name:
            self.sql = f"""
                SELECT * FROM groups WHERE 
                {'id = ' + str(_id) if _id else f"name = '{name}'" if name else "False"}
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

    def create(self, student: dict, returning=False):
        student['group_id'] = self.create_group(student['group_id'])[0]
        student['return_text'] = ''
        if returning:
            student['return_text'] = "RETURNING id"

        self.sql = """
            INSERT INTO students(group_id, first_name, last_name, patronymic, gradebook_identy, telegram_id)  
            VALUES ({group_id}, '{first_name}', '{last_name}', '{patronymic}', '{gradebook}', '{id}')
            {return_text}
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

    def my_course(self):
        self.sql = f"""
            SELECT 
                   c.id,
                   c.name,
                   c.duration,
                   s.start_date,
                   ARRAY_AGG(g.name) AS groups
            FROM courses AS c
                 LEFT JOIN semesters AS s ON s.id = c.semester_id
                 LEFT JOIN "group-cource_rels" AS gr ON gr.cource_id = c.id
                 LEFT JOIN groups AS g ON g.id = gr.group_id
            WHERE c.author = {self.data[0]}
            GROUP BY c.id, c.name, c.duration, c.author, s.start_date
            ORDER BY s.start_date
        """
        return self

    def get_semesters(self, _id=None):
        self.sql = f"""
            SELECT * FROM semesters WHERE TRUE {f'AND {_id} = id' if _id else ''}
        """
        return self

    def create_semesters(self, date_start):
        self.sql = f"""
            INSERT INTO semesters(start_date) VALUES ('{date_start}'::DATE)
            ON CONFLICT DO NOTHING
            RETURNING id
        """
        return self

    def create_course(self, course):
        semester_id = course['semester']
        if course['new']:
            try:
                semester_id = self.create_semesters(course['semester']).commit_return()
                semester_id = semester_id[0]
            except Exception:
                raise MyException('Не удалоь создать семестр.')
        self.sql = f"""
            INSERT INTO courses(name, semester_id, duration, author) 
            VALUES ('{course['name']}', {semester_id}, {course['duration']}, {self.data[0]})
            ON CONFLICT DO NOTHING
        """
        return self

    def check_course(self, course_id):
        self.sql = f"""
            SELECT * FROM courses WHERE id = {course_id} AND author = {self.data[0]}
        """
        return self

    def del_course(self, course_id):
        if not self.check_course(course_id).get():
            raise MyException('Вы не являетесь автором курса')

        self.sql = f"""
            SELECT id FROM lessons WHERE cource_id = {course_id}
        """
        lessons = self.commit_returns()

        if lessons:
            self.sql = f"""
                DELETE FROM "lesson-media_resources_rels" WHERE lesson_id = ANY(ARRAY{lessons})
                RETURNING media_resource_id
            """
            media = self.commit_returns()

            self.sql = f"""
                WITH visible AS (
                    DELETE FROM student_visits WHERE lesson_id = ANY(ARRAY{lessons})
                ),
                point AS (
                    DELETE FROM student_performance WHERE lesson_id = ANY(ARRAY{lessons})
                ),
                lesson AS (
                    DELETE FROM lessons WHERE id = ANY(ARRAY{lessons})
                ) 
                DELETE FROM media_resources WHERE id ANY(ARRAY{media or []}::int)
            """
            self.commit()

        self.sql = f"""
            WITH grp AS (
                DELETE FROM "group-cource_rels" WHERE cource_id = {course_id}
            )
            DELETE FROM courses WHERE id = {course_id}
            RETURNING semester_id
        """

        semester = self.commit_return()
        self.sql = f"""
            SELECT * FROM courses WHERE semester_id = {semester[0]} LIMIT 1
        """

        if not self.get():
            self.sql = f"""
                DELETE FROM semesters WHERE id = {semester[0]}
            """

    def sing_up_course(self, course_id, group):
        if not self.check_course(course_id).get():
            raise MyException('Вы не являетесь автором курса')

        self.sql = f"""
            INSERT INTO "group-cource_rels"(group_id, cource_id) 
            VALUES ({Student().create_group(group)[0]}, {course_id})
        """
        return self

    def create_lesson(self, course, group, _date):
        self.sql = f"""
            INSERT INTO lessons(group_id, cource_id, date_time) 
            VALUES ({group}, {course}, '{_date}'::TIMESTAMP)
            RETURNING id
        """
        return self