import os

from flask import request, send_file
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from werkzeug.security import safe_str_cmp
from models.student_main import StudentMain


class StudentRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('roll_no', type=str, required=True, help='Roll No. is necessary')
    parser.add_argument('reg_no', type=str, required=True, help='Reg No. is necessary')
    parser.add_argument('first_name', type=str, required=True, help='Student first name is necessary')
    parser.add_argument('last_name', type=str, required=True, help='Student last name is necessary')
    parser.add_argument('dob', type=str, required=True, help='Student dob is necessary')
    parser.add_argument('school', type=str, required=True, help='Student school is necessary')
    parser.add_argument('course', type=str, required=True, help='Student course is necessary')
    parser.add_argument('discipline', type=str, required=True, help='Student discipline is necessary')
    parser.add_argument('current_sem', type=str, required=True, help='Student current semester is necessary')
    parser.add_argument('final_sem', type=str, required=True, help='Student final sem is necessary')  # remove later
    parser.add_argument('join_year', type=str, required=True, help='Student join year is necessary')
    parser.add_argument('final_year', type=str, required=True, help='Student final year is necessary')
    parser.add_argument('father_first', type=str)
    parser.add_argument('father_last', type=str)
    parser.add_argument('mother_first', type=str)
    parser.add_argument('mother_last', type=str)
    parser.add_argument('tenth_marks', type=str, required=True, help='Student tenth_marks is necessary')
    parser.add_argument('twelfth_marks', type=str, required=True, help='Student twelfth_marks is necessary')
    parser.add_argument('jee_score', type=str)
    parser.add_argument('password', type=str, required=True, help='Student password is necessary')
    parser.add_argument('phone', type=str, required=True, help='Student phone is necessary')
    parser.add_argument('mail', type=str, required=True, help='Student mail is necessary')
    parser.add_argument('gender', type=str, required=True, help='Student gender is necessary')

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'ppt'])
    IMAGE_ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    UPLOAD_FOLDER_PROFILE_PICTURES = "profile-pictures"
    UPLOAD_FOLDER_PROFILE_PICTURES_PATH = "C:\KRMU_App\database\profile-pictures"

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def post(self):
        data = StudentRegister.parser.parse_args()

        if StudentMain.find_by_roll_number(data['roll_no']):
            return {'message': 'A student with that roll number already exists'}

        file = request.files['file']
        if file.filename == '':
            return {'message': 'The uploaded file has no filename'}
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_name_list = filename.split(".")
            new_file_name = os.path.normpath(os.path.join(self.UPLOAD_FOLDER_PROFILE_PICTURES_PATH, data['roll_no'] +
                                                          "-profile-picture." + file_name_list[len(file_name_list)-1]))
            #  The length function is used for images with multiple '.' in their name.
            #  This makes sure only the last string after the '.' is used that will be the extension
            file.save(new_file_name)
            student = StudentMain(data['roll_no'], data['reg_no'], data['first_name'], data['last_name'], data['dob'],
                                  data['school'], data['course'], data['discipline'], data['current_sem'],
                                  data['final_sem'],
                                  data['join_year'], data['final_year'], data['password'], data['phone'],
                                  data['mail'], data['gender'], data['tenth_marks'], data['twelfth_marks'],
                                  data['jee_score'], data['father_first'], data['father_last'], data['mother_first'],
                                  data['mother_last'], new_file_name)
            student.save_to_db()
            return {
                'message': 'Student registration successful!',
                'data': student.json(),
            }, 201


class StudentProfilePicture(Resource):

    def get(self, roll_no):
        student = StudentMain.find_by_roll_number(roll_no)
        if student:
            filename = "".join(student.get_file_name(roll_no))
            file_list = filename.split(".")
            file_extension = file_list[1]
            file_dictionary = {
                'filename': filename
            }
            return send_file(file_dictionary['filename'], mimetype='image/' + file_extension)


class StudentLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('roll_no', type=str, required=True, help='Roll No. is necessary')
    parser.add_argument('password', type=str, required=True, help='Student password is necessary')

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        student = StudentMain.find_by_roll_number(data['roll_no'])
        if student and safe_str_cmp(student.password, data['password']):
            access_token = create_access_token(identity=student.roll_no, fresh=True)
            refresh_token = create_refresh_token(student.roll_no)
            return {
                'access_token' : access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401