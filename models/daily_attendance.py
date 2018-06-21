import sqlite3

from create_tables_first import STUDENT_DATABASE

DATABASE = STUDENT_DATABASE


class DailyAttendanceModel:

    def __init__(self, roll_no, subject_code, semester, date, day, status):
        self.roll_no = roll_no
        self.subject_code = subject_code
        self.semester = semester
        self.date = date
        self.day = day
        self.status = status

    def save_to_db(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "INSERT INTO daily_attendance values(?,?,?,?,?,?)"
        cursor.execute(query, (self.roll_no, self.subject_code, self.semester, self.date, self.day,self.status,))

        connection.commit()
        connection.close()

