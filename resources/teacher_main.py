import os

from flask import request, send_file
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename
from werkzeug.security import safe_str_cmp
from models.teacher_main import TeacherMain


class TeacherRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("teacher_code", type=str, required=True, help='teacher_code cannot be blank')
    parser.add_argument('teacher_first_name', type=str, required=True, help='teacher_first_name cannot be blank')
    parser.add_argument('teacher_last_name', type=str, required=True, help='teacher_last_name cannot be blank')
    parser.add_argument('department', type=str, required=True, help='department cannot be blank')
    parser.add_argument('employment_status', type=str, required=True, help='employment_status cannot be blank')

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'ppt'])
    IMAGE_ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    UPLOAD_FOLDER_PROFILE_PICTURES_PATH = "C:\KRMU_App\database\profile-pictures"

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def post(self):
        data = TeacherRegister.parser.parse_args()

        if TeacherMain.find_by_teacher_code(data['teacher_code']):
            return {'message': 'A teacher with that teacher code already exists'}

        file = request.files['file']
        if file.filename == '':
            return {'message': 'The uploaded file has no filename'}
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_name_list = filename.split(".")
            new_file_name = os.path.normpath(os.path.join(self.UPLOAD_FOLDER_PROFILE_PICTURES_PATH, data['teacher_code'] +
                                                          "-profile-picture-teacher." +
                                                          file_name_list[len(file_name_list)-1]))
            #  The length function is used for images with multiple '.' in their name.
            #  This makes sure only the last string after the '.' is used that will be the extension
            file.save(new_file_name)
            student = TeacherMain(data['teacher_code'], data['teacher_first_name'], data['teacher_last_name'],
                                  data['department'], data['employment_status'], new_file_name)
            student.save_to_db()
            return {
                'message': 'Teacher registration successful!',
                'data': student.json(),
            }, 201


class TeacherProfilePicture(Resource):

    def get(self, teacher_code):
        teacher = TeacherMain.find_by_teacher_code(teacher_code)
        if teacher:
            filename = "".join(teacher.get_file_name(teacher_code))
            file_list = filename.split(".")
            file_extension = file_list[1]
            file_dictionary = {
                'filename': filename
            }
            return send_file(file_dictionary['filename'], mimetype='image/' + file_extension)
