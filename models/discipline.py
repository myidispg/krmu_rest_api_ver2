import sqlite3

from create_tables_first import SCHOOLS_DATABASE

DATABASE = SCHOOLS_DATABASE


class Discipline:

    def __init__(self, course, discipline, duration_sem, school):
        self.course = course
        self.discipline = discipline
        self.duration_sem = duration_sem
        self.school = school

