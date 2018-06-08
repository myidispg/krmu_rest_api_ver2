import sqlite3

STUDENT_DATABASE = 'C:\KRMU_App\database\main_student_database.db'
TEACHER_DATABASE = 'C:\KRMU_App\database\main_teacher_database.db'

connection = sqlite3.connect(STUDENT_DATABASE)
cursor = connection.cursor()

create_table_student = "CREATE TABLE IF NOT EXISTS student_main" \
                       "(roll_no text, reg_no text, first_name text, last_name text, dob text, school text," \
                       "course text, discipline text," \
                       " current_sem int, final_sem int, join_year int, final_year int, father_first_name text," \
                       " father_last_name text, mother_first_name text, mother_last_name text, tenth_marks real," \
                       "twelfth_marks real, jee_score real, image text, password text, phone text, mail text, gender text)"

cursor.execute(create_table_student)

connection.commit()
connection.close()

connection = sqlite3.connect(TEACHER_DATABASE)
cursor = connection.cursor()


create_table_teacher = "CREATE TABLE IF NOT EXISTS teacher_main (teacher_code text, teacher_first_name text," \
                       " teacher_last_name text, password text, department text, employment_status text, image text)"

cursor.execute(create_table_teacher)

connection.commit()
connection.close()