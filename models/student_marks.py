import sqlite3

from create_tables_first import STUDENT_DATABASE

DATABASE = STUDENT_DATABASE


class StudentMarks:

    def __init__(self, roll_no, subject_code, semester, cat, mid, end, assignment, attendance):
        self.roll_no = roll_no
        self.subject_code = subject_code
        self.semester = semester
        self.cat = cat
        self.mid = mid
        self.end = end
        self.assignment = assignment
        self.attendance = attendance

    @classmethod
    def get_marks_all(cls, subject_code, roll_no, semester):
        connection = sqlite3.connect(STUDENT_DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM student_marks WHERE roll_no = ? AND subject_code = ? AND semester =?"
        result = cursor.execute(query, (roll_no, subject_code, semester,))

        row = result.fetchone()
        if row is not None:
            row_list = list(row)
            for i in range(3, 8):
                if row_list[i] is None:
                    row_list[i] = 0
                    row = tuple(row_list)
            return {
                'subject_code': subject_code,
                'cat': row[3],
                'mid': row[4],
                'end': row[5],
                'assignment': row[6],
                'attendance': row[7]
            }
        else:
            return {
                'subject_code': subject_code,
                'cat': 0,
                'mid': 0,
                'end': 0,
                'assignment': 0,
                'attendance': 0
            }
