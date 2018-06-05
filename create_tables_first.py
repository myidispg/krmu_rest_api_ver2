import sqlite3

connection = sqlite3.connect('main_student_database.db')
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

