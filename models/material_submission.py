import sqlite3

from create_tables_first import SCHOOLS_DATABASE

DATABASE = SCHOOLS_DATABASE


class MaterialSubmissionResource:

    def __init__(self, material_code, student_roll_no, submission_date, marks_obtained, submission_path):
        self.material_code = material_code
        self.student_roll_no = student_roll_no
        self.submission_date = submission_date
        self.marks_obtained = marks_obtained
        self.submission_path = submission_path

    def save_to_db(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "INSERT INTO material_submission values (?, ?, ?, ?, ?)"
        cursor.execute(query, (self.material_code, self.student_roll_no, self.submission_date, self.marks_obtained,
                               self.submission_path,))

        connection.commit()
        connection.close()