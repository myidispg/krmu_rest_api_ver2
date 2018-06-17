import sqlite3

from create_tables_first import SCHOOLS_DATABASE

DATABASE = SCHOOLS_DATABASE


class TimeTableModel:

    def __init__(self, subject_code, day, start_time, end_time, teacher_code):
        self.subject_code = subject_code
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.teacher_code = teacher_code

    @staticmethod
    def get_all_by_subject_code(subject_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM time_table WHERE subject_code = ?"
        result = cursor.execute(query, (subject_code,))

        rows = result.fetchall()
        row_list = []
        for row in rows:
            time_table = TimeTableModel(row[0], row[1], row[2], row[3], row[4])
            row_list.append(time_table)
        connection.close()
        return row_list

    @staticmethod
    def get_all_by_teacher_code(teacher_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM time_table WHERE teacher_code = ?"
        result = cursor.execute(query, (teacher_code,))

        rows = result.fetchall()
        row_list = []
        for row in rows:
            time_table = TimeTableModel(row[0], row[1], row[2], row[3], row[4])
            row_list.append(time_table)
        connection.close()
        return row_list



