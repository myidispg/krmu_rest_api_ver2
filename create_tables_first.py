import sqlite3

STUDENT_DATABASE = 'C:\KRMU_App\database\main_student_database.db'
TEACHER_DATABASE = 'C:\KRMU_App\database\main_teacher_database.db'
SCHOOLS_DATABASE = 'C:\KRMU_App\database\schools_database.db'


#  create tables to go into STUDENTS database
connection = sqlite3.connect(STUDENT_DATABASE)
cursor = connection.cursor()

create_table_student = "CREATE TABLE IF NOT EXISTS student_main" \
                       "(roll_no text, reg_no text, first_name text, last_name text, dob text, school text," \
                       "course text, discipline text," \
                       " current_sem int, final_sem int, join_year int, final_year int, father_first_name text," \
                       " father_last_name text, mother_first_name text, mother_last_name text, tenth_marks real," \
                       "twelfth_marks real, jee_score real, image text, password text, phone text, mail text," \
                       " gender text)"

create_table_student_attendance = "CREATE TABLE IF NOT EXISTS student_attendance (roll_no text, subject_code text," \
                                  " semester integer, max_attendance int, present_attendance int)"
create_table_student_marks = "CREATE TABLE IF NOT EXISTS student_marks (roll_no text, subject_code text, " \
                             "semester int, cat real, mid real, end real, assignment real, attendance real)"

cursor.execute(create_table_student)
cursor.execute(create_table_student_attendance)
cursor.execute(create_table_student_marks)

connection.commit()
connection.close()

#  create tables to go into TEACHERS database
connection = sqlite3.connect(TEACHER_DATABASE)
cursor = connection.cursor()


create_table_teacher = "CREATE TABLE IF NOT EXISTS teacher_main (teacher_code text, teacher_first_name text," \
                       " teacher_last_name text, password text, department text, employment_status text, image text)"

cursor.execute(create_table_teacher)

connection.commit()
connection.close()

#  create tables to go into SCHOOLS database
connection = sqlite3.connect(SCHOOLS_DATABASE)
cursor = connection.cursor()

create_table_schools = "CREATE TABLE IF NOT EXISTS schools (school_code text, school_name text, course text)"
create_table_discipline = "CREATE TABLE IF NOT EXISTS disciplines(course text, discipline text, duration_sem integer," \
                          " school text)"
create_table_subjects = "CREATE TABLE IF NOT EXISTS subjects(discipline text, subject_code text, subject_name text," \
                        " elective integer, taught_in_sem integer, lectures integer, tutorials integer," \
                        " practicals integer, credits integer)"
create_table_time_table = "CREATE TABLE IF NOT EXISTS time_table (subject_code text, subject_name text," \
                          " teacher_first text, teacher_last text, discipline text, semester integer," \
                          " day text, start_time text, end_time text)"
create_table_material_upload = "CREATE TABLE IF NOT EXISTS material_teacher_upload (teacher_code text," \
                               " material_code text, upload_date text, course text," \
                                " discipline text, subject_code text, semester integer, deadline_date text," \
                                " type text, material_path text)"
create_table_material_submissions = "CREATE TABLE IF NOT EXISTS material_submission (material_code text, " \
                                       "student_roll_no text, submission_date text, marks_obtained integer," \
                                       " submission_path text)"


cursor.execute(create_table_schools)
cursor.execute(create_table_discipline)
cursor.execute(create_table_subjects)
cursor.execute(create_table_time_table)
cursor.execute(create_table_material_upload)
cursor.execute(create_table_material_submissions)

connection.commit()
connection.close()
