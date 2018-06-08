import sqlite3

from create_tables_first import SCHOOLS_DATABASE

DATABASE = SCHOOLS_DATABASE


class Schools:

    def __init__(self, school_code, school_name, course, course_type):
        self.school_code = school_code
        self.school_name = school_name
        self.course = course
        self.course_type = course_type


