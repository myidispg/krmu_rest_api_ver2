import sqlite3

from create_tables_first import STUDENT_DATABASE

DATABASE = STUDENT_DATABASE


class StudentAttendance:

    def __init__(self, roll_no, subject_code, semester, max_attendance, present_attendance):
        self.roll_no = roll_no
        self.subject_code = subject_code
        self.semester = semester
        self.max_attendance = max_attendance
        self.present_attendance = present_attendance

    @classmethod
    def get_attendance_max_present(cls, subject_code, roll_no, semester):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT max_attendance, present_attendance FROM student_attendance WHERE subject_code = ?" \
                " AND roll_no = ? AND semester = ?"
        result = cursor.execute(query, (subject_code, roll_no, semester,))

        row = result.fetchall()

        for column in row:
                return {
                    'subject_code': subject_code,
                    'max_attendance': column[0],
                    'present_attendance': column[1]
                }
        return None

