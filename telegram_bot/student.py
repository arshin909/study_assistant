
from telegram_bot.config import db_connect, COURSE_LIFE
from telebot.types import Message


class People:

    table = None

    def get_people(self, data: Message):
        """ Записан студетн или нет """
        sql = f"""
            SELECT * FROM {self.table}
            WHERE telegram_id = '{data.from_user.id}' 
            LIMIT 1
        """

        with db_connect.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()

        return result


class Student(People):
    type_ = 1
    table = 'students'

    def create_group(self, group):

        sql = f"""
            INSERT INTO groups(name) VALUES ('{group}')
            ON CONFLICT DO NOTHING 
        """

        with db_connect.cursor() as cursor:
            cursor.execute(sql)
            cursor.execute(f"SELECT id FROM groups WHERE name = '{group}' LIMIT 1")
            result = cursor.fetchone()
            db_connect.commit()

        return result[0]

    def create_student(self, data: Message):
        from_user = data.from_user
        sql = f"""
            INSERT INTO students(group_id, first_name, last_name, patronymic, gradebook_identy, telegram_id)  
            VALUES ({self.create_group(from_user.group_id)}, '{from_user.first_name}', '{from_user.last_name}', 
                    '{from_user.patronymic}', '{from_user.gradebook}', '{from_user.id}')
        """
        with db_connect.cursor() as cursor:
            cursor.execute(sql)
            db_connect.commit()

    def cource_list(self):

        sql = f"""
            SELECT courses.name, semesters.start_date
            FROM courses, semesters 
            WHERE 
                courses.semester_id = semesters.id AND
                semesters.start_date + interval '{COURSE_LIFE}' >= date_trunc('day', now()) 
        """
        with db_connect.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

        return result
