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

    @staticmethod
    def get_material_by_material_code(material_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * from material_teacher_upload WHERE material_code = ?"
        result = cursor.execute(query, (material_code,))

        row = result.fetchone()
        material = {
            'teacher_code': row[0],
            material_code: material_code,
            'upload_date': row[2],
            'course': row[3],
            'discipline': row[4],
            'subject_code': row[5],
            'semester': row[6],
            'deadline_date': row[7],
            'type': row[8],
            'material_path': row[9]
        }
        connection.close()
        return material

    @staticmethod
    def get_material_path_by_material_code(material_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT material_path from material_teacher_upload WHERE material_code = ?"
        result = cursor.execute(query, (material_code,))

        row = result.fetchone()

        row = ''.join(row)

        connection.close
        return row

    @staticmethod
    def get_all_by_teacher_code(teacher_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * from material_teacher_upload WHERE teacher_code = ?"
        result = cursor.execute(query, (teacher_code,))

        rows = result.fetchall()
        row_list = []
        for row in rows:
            dictionary = {
                'material_code': row[1],
                'upload_date': row[2],
                'course': row[3],
                'discipline': row[4],
                'subject_code': row[5],
                'semester': row[6],
                'deadline_date': row[7],
                'type': row[8],
                'material_path': row[9]
            }
            row_list.append(dictionary)
        connection.close()
        return row_list

    @staticmethod
    def get_all_by_discipline_semester(discipline, semester):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * from material_teacher_upload WHERE discipline = ? AND semester = ?"
        result = cursor.execute(query, (discipline, semester,))

        rows = result.fetchall()
        row_list = []
        for row in rows:
            dictionary = {
                'material_code': row[1],
                'upload_date': row[2],
                'course': row[3],
                'discipline': row[4],
                'subject_code': row[5],
                'semester': row[6],
                'deadline_date': row[7],
                'type': row[8],
                'material_path': row[9]
            }
            row_list.append(dictionary)
        connection.close()
        return row_list

    def save_to_db(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "INSERT INTO material_teacher_upload values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (self.teacher_code, self.material_code, self.upload_date, self.course, self.discipline,
                               self.subject_code, self.semester, self.deadline_date, self.material_type,
                               self.material_path,))

        connection.commit()
        connection.close()



