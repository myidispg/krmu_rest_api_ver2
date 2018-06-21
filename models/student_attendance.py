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

        row = result.fetchone()
        if row is not None:
            return {
                'subject_code': subject_code,
                'max_attendance': row[0],
                'present_attendance': row[1]
            }
        else:
            return {
                    'subject_code': subject_code,
                    'max_attendance': 0,
                    'present_attendance': 0
            }

    @classmethod
    def set_attendance(cls, subject_code, semester, roll_no, status):
        semester = int(semester)
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query_check_presence = "SELECT * FROM student_attendance WHERE roll_no = ? AND subject_code = ?" \
                               " AND semester = ?"
        result = cursor.execute(query_check_presence, (roll_no, subject_code, semester))
        row = result.fetchone()
        if row is not None:
            if status == 'P':
                query_update_attendance_present = "UPDATE student_attendance SET" \
                                                  " present_attendance = present_attendance + 1," \
                                                  " max_attendance = max_attendance + 1 WHERE roll_no = ? AND" \
                                                  " subject_code = ? AND semester = ?"
                cursor.execute(query_update_attendance_present, (roll_no, subject_code, semester,))
            else:
                if status == 'A':
                    query_update_attendance_absent = "UPDATE student_attendance SET  " \
                                                     "max_attendance = max_attendance + 1" \
                                                     " WHERE roll_no = ? AND" \
                                                     " subject_code = ? AND semester = ?"
                    cursor.execute(query_update_attendance_absent, (roll_no, subject_code, semester,))
        else:
            if status == 'P':
                query_insert_attendance = "INSERT INTO student_attendance values " \
                                              "(?,?,?,1,1)"
                cursor.execute(query_insert_attendance, (roll_no, subject_code, semester,))
            else:
                query_insert_attendance_1 = "INSERT INTO student_attendance values " \
                                              "(?,?,?,1,0)"
                cursor.execute(query_insert_attendance_1, (roll_no, subject_code, semester,))
        connection.commit()
        connection.close()
        return {'message': 'attendance updated'}
