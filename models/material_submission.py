import sqlite3

from create_tables_first import SCHOOLS_DATABASE

DATABASE = SCHOOLS_DATABASE


class MaterialSubmissionModel:

    def __init__(self, material_code, student_roll_no, submission_date, marks_obtained, submission_path):
        self.material_code = material_code
        self.student_roll_no = student_roll_no
        self.submission_date = submission_date
        self.marks_obtained = marks_obtained
        self.submission_path = submission_path

    @staticmethod
    def add_student_submission(submission_date, submission_path, material_code, student_roll_no):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "UPDATE material_submission SET submission_date = ? , submission_path = ? WHERE material_code = ?" \
                " AND student_roll_no = ?"
        cursor.execute(query, (submission_date, submission_path, material_code, student_roll_no))

        connection.commit()
        connection.close()

    @staticmethod
    def add_student_marks(material_code, student_roll_no, marks_obtained):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "UPDATE material_submission SET marks_obtained = ? WHERE material_code = ? AND student_roll_no = ?"
        cursor.execute(query, (marks_obtained, material_code, student_roll_no,))

        connection.commit()
        connection.close()

    @staticmethod
    def get_all_by_material_code(material_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM material_submission WHERE material_code = ?"
        result = cursor.execute(query, (material_code,))

        rows = result.fetchall()
        row_list = []
        for row in rows:
            dictionary = {
                'student_roll_no': row[1],
                'submission_date': row[2],
                'marks_obtained': row[3]
            }
            row_list.append(dictionary)
        connection.close()
        return row_list

    @staticmethod
    def get_submission_date_by_material_code(material_code, roll_no):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT submission_date from material_submission where material_code = ? AND student_roll_no = ?"
        result = cursor.execute(query, (material_code, roll_no,))

        row = result.fetchone()
        if row[0] is not None:
            row = "".join(row)
        else:
            row = "None"
        return row

    def save_to_db(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "INSERT INTO material_submission values (?, ?, ?, ?, ?)"
        cursor.execute(query, (self.material_code, self.student_roll_no, self.submission_date, self.marks_obtained,
                               self.submission_path,))

        connection.commit()
        connection.close()