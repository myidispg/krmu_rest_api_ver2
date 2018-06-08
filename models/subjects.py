import sqlite3

from create_tables_first import SCHOOLS_DATABASE

DATABASE = SCHOOLS_DATABASE


class Subjects:

    def __init__(self, discipline, subject_code, subject_name, elective, taught_in_sem, lectures, tutorials,
                 practicals, total_credits):
        self.discipline = discipline
        self.subject_code = subject_code
        self.subject_name = subject_name
        self.elective = elective
        self.taught_in_sem = taught_in_sem
        self.lectures = lectures
        self.tutorials = tutorials
        self.practicals = practicals
        self.total_credits = total_credits

    @classmethod
    def find_subject(cls, discipline, current_sem):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM subjects WHERE discipline = ? AND taught_in_sem = ?"
        result = cursor.execute(query, (discipline, current_sem,))

        row = result.fetchall()

        subjects_code_list = []

        if row is not None:
            for each_row in row:
                subjects_code_list.append(each_row[1])

        connection.close()

        return subjects_code_list


