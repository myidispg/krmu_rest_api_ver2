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

    @staticmethod
    def change_daily_attendance(roll_no, subject_code, date):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT status from daily_attendance WHERE roll_no = ? AND subject_code = ? AND date=?"
        result = cursor.execute(query, (roll_no, subject_code, date,))

        rows = result.fetchall()
        counter = 0
        absent_flag = False  # this is used to see whether there is an absent case or not.
        # If there is no absent case, the update query will not execute
        for row in rows:
            if row[0] == 'A':
                counter += 1
                absent_flag = True
        if absent_flag is True:
            query_update = "UPDATE daily_attendance SET status = ? WHERE roll_no = ?AND subject_code = ?" \
                           " AND date=?"
            cursor.execute(query_update, ('P', roll_no, subject_code, date))
            connection.commit()
        connection.close()
        return {
            'update_happened': absent_flag,
            'counter': counter
        }

    def save_to_db(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "INSERT INTO daily_attendance values(?,?,?,?,?,?)"
        cursor.execute(query, (self.roll_no, self.subject_code, self.semester, self.date, self.day,self.status,))

        connection.commit()
        connection.close()

