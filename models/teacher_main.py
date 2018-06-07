import sqlite3
from create_tables_first import DATABASE

DATABASE = DATABASE


class TeacherMain:

    def __init__(self, teacher_code, teacher_first_name, teacher_last_name, department, employment_status, image):
        self.teacher_code = teacher_code
        self.teacher_first_name = teacher_first_name
        self.teacher_last_name = teacher_last_name
        self.department = department
        self.employment_status = employment_status
        self.image = image

    @classmethod
    def find_by_teacher_code(cls, teacher_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM teacher_main WHERE teacher_code=?"
        result = cursor.execute(query, (teacher_code,))

        row = result.fetchone()
        if row is not None:
            teacher = cls(row[0], row[1], row[2]. row[3], row[5], row[6])
        else:
            teacher = None

        connection.close()
        return teacher

    def save_to_db(self):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "INSERT INTO teacher_main VALUES(?, ?, ?, ?, ?, ?)"

        cursor.execute(query, (self.teacher_code, self.teacher_first_name, self.teacher_last_name, self.department,
                               self.employment_status, self.image))

        connection.commit()
        connection.close()

    @classmethod
    def get_file_name(cls, teacher_code):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT image FROM teacher_main WHERE teacher_code=?"
        result = cursor.execute(query, (teacher_code,))

        filename = result.fetchone()
        if filename is not None:
            connection.close()
            return filename
        connection.close()
        return False

    def json(self):
        return {
            'teacher_code': self.teacher_code,
            'teacher_first_name': self.teacher_first_name,
            'teacher_last_name': self.teacher_last_name,
            'department': self.department,
            'employment_status': self.employment_status,
        }

