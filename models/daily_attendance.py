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

    @staticmethod
    def get_daily_attendance_by_roll_sub_code(roll_no, subject_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM daily_attendance WHERE roll_no = ? AND subject_code = ?"
        result = cursor.execute(query, (roll_no, subject_code,))

        rows = result.fetchall()
        daily_attendance_list = []
        for row in rows:
            dictionary = {
                'semester': row[2],
                'date': row[3],
                'day': row[4],
                'status': row[5]
            }
            daily_attendance_list.append(dictionary)
        connection.close()
        return daily_attendance_list


    def save_to_db(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "INSERT INTO daily_attendance values(?,?,?,?,?,?)"
        cursor.execute(query, (self.roll_no, self.subject_code, self.semester, self.date, self.day,self.status,))

        connection.commit()
        connection.close()

