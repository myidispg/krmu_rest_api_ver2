import sqlite3
from create_tables_first import DATABASE

DATABASE = DATABASE


class StudentMain:

    def __init__(self, roll_no, reg_no, first_name, last_name, dob, school, course, discipline, current_sem, final_sem,
                 join_year, final_year, password, phone, mail, gender, tenth_marks, twelfth_marks, jee_score,
                 father_first=None, father_last=None, mother_first=None, mother_last=None, image_path=None):
        self.roll_no = roll_no
        self.reg_no = reg_no
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.school = school
        self.course = course
        self.discipline = discipline
        self.current_sem = current_sem
        self.final_sem = final_sem
        self.join_year = join_year
        self.final_year = final_year
        self.father_first = father_first
        self.father_last = father_last
        self.mother_first = mother_first
        self.mother_last = mother_last
        self.tenth_marks = tenth_marks
        self.twelfth_marks = twelfth_marks
        self.jee_score = jee_score
        self.image_path = image_path
        self.password = password
        self.phone = phone
        self.mail = mail
        self.gender = gender

    @classmethod
    def find_by_roll_number(cls, roll_no):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM student_main WHERE roll_no=?"
        result = cursor.execute(query, (roll_no,))

        row = result.fetchone()
        if row is not None:
            student = cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                          row[11], row[16], row[17], row[18], row[20], row[21], row[22], row[23], row[12], row[13],
                          row[14], row[15], row[19])
        else:
            student = None

        connection.close()
        return student

    @classmethod
    def find_by_reg_number(cls, reg_no):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT * FROM student_main WHERE reg_no=?"
        result = cursor.execute(query, (reg_no,))

        row = result.fetchone()
        if row is not None:
            student = cls(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                          row[11], row[16], row[17], row[18], row[20], row[21], row[22], row[23], row[12], row[13],
                          row[14], row[15], row[19])
        else:
            student = None

        connection.close()
        return student

    @classmethod
    def get_file_name(cls, roll_no):
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "SELECT image FROM student_main WHERE roll_no=?"
        result = cursor.execute(query, (roll_no,))

        filename = result.fetchone()
        if filename is not None:
            connection.close()
            return filename
        connection.close()
        return False

    def save_to_db(self):  # this method requires an object of StudentMain class to be already created
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        query = "INSERT INTO student_main VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?," \
                " ?, ?, ?)"

        cursor.execute(query, (self.roll_no, self.reg_no, self.first_name, self.last_name, self.dob, self.school,
                               self.course, self.discipline, self.current_sem, self.final_sem, self.join_year,
                               self.final_year, self.father_first, self.father_last, self.mother_first,
                               self.mother_last, self.tenth_marks, self.twelfth_marks, self.jee_score, self.image_path,
                               self.password, self.phone, self.mail, self.gender))

        connection.commit()
        connection.close()

    def json(self):
        return {
            'roll_no': self.roll_no,
            'reg_no': self.reg_no,
            'student_first_name': self.first_name,
            'student_last_name': self.last_name,
            'dob': self.dob,
            'school': self.school,
            'course': self.course,
            'discipline': self.discipline,
            'current_sem': self.current_sem,
            'final_sem': self.final_sem,
            'join_year': self.join_year,
            'final_year': self.final_year,
            'father_first_name': self.father_first,
            'father_last_name': self.father_last,
            'mother_first_name': self.mother_first,
            'mother_last_name': self.mother_last,
            'tenth_marks': self.tenth_marks,
            'twelfth_marks': self.twelfth_marks,
            'jee_score': self.jee_score,
            'student_phone': self.phone,
            'student_mail': self.mail,
            'student_gender': self.gender
        }
