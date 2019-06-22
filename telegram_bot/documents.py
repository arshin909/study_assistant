import io
import xlwt, openpyxl
from re import compile
from datetime import timedelta
import datefinder

from telegram_bot.request_db import Teacher, MyException
from telegram_bot.helpers import format_group
from telegram_bot.request_db import Student


class Attachment(Teacher):
    fields_state = ('ID студента', 'Имя студента', 'Номер зачетки')

    def __sql_get_state(self, course_id, group_id):
        self.sql = f"""
            SELECT
                s.id, 
                initcap(concat(s.last_name, ' ', s.first_name, ' ', s.patronymic)) as student,
                s.gradebook_identy,
                l.date_time,
                v.visited, 
                p.points
            FROM
                lessons AS l
                LEFT JOIN student_visits AS v ON v.lesson_id = l.id
                LEFT JOIN student_performance AS p ON p.lesson_id = v.lesson_id AND p.student_id = v.student_id
                LEFT JOIN students AS s ON s.id = v.student_id
            WHERE 
                l.cource_id = {course_id}
                AND l.group_id = {group_id}
            ORDER BY 
                l.date_time
        """
        return self

    def get_state(self, course, group):
        group_info = self.get_group(name=group).get()
        if not group_info:
            raise MyException('Не найдена группа с таким номером.')

        course_info = self.check_course(course).get()
        if not course_info:
            raise MyException('Не найден курс с таким номером.')

        state = self.__sql_get_state(course_info[0], group_info[0]).all()
        if not state:
            raise MyException('Не найденны проведенные занятия.')

        file = xlwt.Workbook('utf-8')
        sheet = file.add_sheet(group)
        date_field = tuple({i[3].strftime('%Y-%m-%d %H:%M') for i in state})
        for index, field in enumerate(self.fields_state + date_field):
            sheet.write(0, index, field)

        data = {}
        for row in state:
            value = row[5] or ('+' if row[4] else '-')
            key = row[3].strftime('%Y-%m-%d %H:%M')
            data.setdefault(tuple(row[:3]), {})[key] = value

        for line, (key, value) in enumerate(sorted(data.items()), start=1):
            if len(value) != len(date_field):
                raise MyException('Ошибка при формировании документа.')

            for column, field in enumerate(key):
                if field is None:
                    field = ''
                sheet.write(line, column, field)
            for column, (_, field) in enumerate(sorted(value.items()), start=len(key)):
                sheet.write(line, column, str(field))

        result = io.BytesIO()
        file.save(result)
        result.seek(0)
        result.name = f"{course_info[1]}_{group_info[1]}.xlsx"
        return result

    def write_state(self, file, course):
        course_info = self.check_course(course).get()
        if not course_info:
            raise MyException('Не найден курс с таким номером.')

        text_error = ""

        wb = openpyxl.load_workbook(io.BytesIO(file))
        groups = {format_group(i): i for i in wb.get_sheet_names()}
        self.sql = f"""
            SELECT name FROM "group-cource_rels", groups WHERE cource_id = {course} AND group_id=id
        """
        for name in {i for (i,) in self.all()} & set(groups.keys()):
            sheet = wb.get_sheet_by_name(groups[name])
            first_data, last_data = {}, {}
            dates = []

            for row in sheet.values:
                if not dates:
                    dates = list(filter(bool, row[3:]))
                    continue

                key = tuple(row[:3])
                first_data[key] = tuple(row[3:])
            group_data = Student().create_group(name)
            self.sql = f"""
                SELECT
                id,
                concat(last_name, first_name, patronymic) as fio,
                gradebook_identy
                FROM students 
                WHERE group_id = {group_data[0]}
            """
            students = self.all()
            for stud in first_data.keys():
                check_id = lambda x: x[0] == stud[0]
                check_number = lambda x: x[2] == str(stud[2]).replace(' ', '')
                check_name = lambda x: x[1].lower() == str(stud[1]).replace(' ', '').lower()

                be = None
                if stud[0]:
                    be = [i for i in students if check_id(i)]
                elif stud[2]:
                    be = [i for i in students if check_number(i)]
                elif stud[1]:
                    be = [i for i in students if check_name(i)]

                if be and len(be) == 1:
                    new_key = list(stud)
                    new_key[0] = be[0][0]
                    last_data[tuple(new_key)] = first_data[stud]
                elif not be and stud[1] and stud[2]:
                    r = compile(r'^[ \n]*(?P<fio>[\w]+ [\w]+ [\w]+)[ \n]*$')
                    fio = r.search(stud[1])
                    if fio:
                        fio = fio.group('fio').split(' ')
                        student = {
                            'last_name': fio[0],
                            'first_name': fio[1],
                            'patronymic': fio[2],
                            'id': None
                        }
                        try:
                            gradebook = int(stud[2])
                        except (ValueError, TypeError):
                            text_error += f'Номер зачетки должен быть числом. {stud[2]} \n'
                            continue
                        student.update({
                            'group_id': name,
                            'gradebook': gradebook,
                        })
                        new_key = list(stud)
                        new_key[0] = Student().create(student, True).commit_return()[0]
                        last_data[tuple(new_key)] = first_data[stud]
                else:
                    text_error += f"Не удалось однозначно определить студента {stud}) \n"

            if not last_data:
                continue

            self.sql = f"""
                SELECT id, date_time
                FROM lessons
                WHERE 
                    cource_id = {course} AND 
                    group_id = {group_data[0]}
            """
            all_lesson = self.all()

            last_date = {}
            for lesson in dates:
                date_lesson = list(datefinder.find_dates(lesson))

                if not date_lesson:
                    last_date[lesson] = None
                    continue

                check = [i for i in all_lesson
                         if i[1] - timedelta(minutes=20) <= date_lesson[0] <= i[1] + timedelta(minutes=20)]

                print(check)
                if check:
                    last_date[lesson] = check[0][0]
                else:
                    last_date[lesson] = self.create_lesson(course, group_data[0], lesson).commit_return()[0]
                    self.sql = f""" 
                        INSERT INTO student_visits(student_id, lesson_id, visited) 
                        VALUES {','.join(f'({i[0]}, {last_date[lesson]}, false)' for i in students)}
                        ON CONFLICT DO NOTHING
                    """
                    self.commit()

            for stud, values in last_data.items():
                for index, val in enumerate(values):

                    if not val or not last_date[dates[index]]:
                        continue

                    if isinstance(val, int):
                        self.sql = f"""
                            INSERT INTO student_performance(student_id, lesson_id, points)
                            VALUES ({stud[0]}, {last_date[dates[index]]}, {val})
                            ON CONFLICT (student_id, lesson_id) DO UPDATE SET points = EXCLUDED.points
                        """
                        self.commit()

                    self.sql = f"""
                        INSERT INTO student_visits(student_id, lesson_id, visited)
                        VALUES ({stud[0]}, {last_date[dates[index]]}, {val != '-'})
                        ON CONFLICT (student_id, lesson_id) DO UPDATE SET visited = EXCLUDED.visited
                    """
                    self.commit()

        return text_error
