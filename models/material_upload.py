import sqlite3

from create_tables_first import SCHOOLS_DATABASE

DATABASE = SCHOOLS_DATABASE


class MaterialUploadModel:

    def __init__(self, teacher_code, material_code, upload_date, course, discipline,
                 subject_code, semester, deadline_date, material_type, material_path):
        self.teacher_code = teacher_code
        self.upload_date = upload_date
        self.course = course
        self.discipline = discipline
        self.subject_code = subject_code
        self.semester = semester
        self.deadline_date = deadline_date
        self.material_type = material_type
        self.material_code = material_code
        self.material_path = material_path

    @classmethod
    def material_already_exists(cls, material_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM material_teacher_upload WHERE material_code = ?"
        result = cursor.execute(query, (material_code,))
        row = result.fetchone()
        if row is None:
            return False
        else:
            return True

    @classmethod
    def get_material_counter(cls, material_code_without_counter):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT material_code from material_teacher_upload WHERE material_code LIKE ?"
        result = cursor.execute(query, (material_code_without_counter + '%',))

        row = result.fetchall()
        highest_counter = 0
        for each_row in row:
            each_row_string = ''.join(each_row)
            words_list = each_row_string.split('-')
            old_counter = words_list[len(words_list)-1]
            old_counter = int(old_counter)
            if old_counter > highest_counter:
                highest_counter = old_counter
        return str(highest_counter+1)

    def save_to_db(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "INSERT INTO material_teacher_upload values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (self.teacher_code, self.material_code, self.upload_date, self.course, self.discipline,
                               self.subject_code, self.semester, self.deadline_date, self.material_type,
                               self.material_path,))

        connection.commit()
        connection.close()



