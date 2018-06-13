import sqlite3

from create_tables_first import SCHOOLS_DATABASE

DATABASE = SCHOOLS_DATABASE


class Discipline:

    def __init__(self, course, discipline, duration_sem, school):
        self.course = course
        self.discipline = discipline
        self.duration_sem = duration_sem
        self.school = school

    @staticmethod
    def get_short_form(discipline):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT short_form FROM disciplines WHERE discipline = ?"
        result = cursor.execute(query, (discipline,))

        row = result.fetchone()
        connection.close()
        row_string = ''.join(row)
        return row_string


