import os

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename

from models.material_upload import MaterialUploadModel


class MaterialUploadResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('teacher_code', type=str, required=True, help='teacher_code cannot be blank')
    parser.add_argument('upload_date', type=str, required=True, help='upload_date cannot be blank')
    parser.add_argument('course', type=str, required=True, help='course cannot be blank')
    parser.add_argument('discipline', type=str, required=True, help='discipline cannot be blank')
    parser.add_argument('subject_code', type=str, required=True, help='subject_code cannot be blank')
    parser.add_argument('semester', type=str, required=True, help='semester cannot be blank')
    parser.add_argument('deadline_date', type=str, required=False)
    parser.add_argument('material_type', type=str, required=False)

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'ppt', 'docx'])
    UPLOAD_FOLDER_ASSIGNMENTS_PATH = "C:\KRMU_App\database\study-material"

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def generate_material_code(self, discipline, semester, subject_code, material_type, counter):
        code = discipline + "-" + semester + '-' + subject_code + '-' + material_type + '-' + counter
        return code

    def post(self):
        data = MaterialUploadResource.parser.parse_args()

        # material_code = self.generate_material_code(data['discipline'], data['semester'],
        #                                             data['subject_code'], data['material_type'], '1')
        #
        # if MaterialUploadModel.material_already_exists(material_code):
        #     counter = material_code.split('-')
        #     end_index = len(counter)
        #     new_counter = str(int(counter[end_index-1]) + 1)
        #     material_code = self.generate_material_code(data['discipline'], data['semester'],
        #                                                                   data['subject_code'], data['material_type'],
        #                                                                   new_counter)

        latest_counter = MaterialUploadModel.get_material_counter(data['discipline'] + "-" + data['semester']
                                                                  + '-' + data['subject_code'] + '-' +
                                                                  data['material_type'])
        material_code = self.generate_material_code(data['discipline'], data['semester'],
                                                    data['subject_code'], data['material_type'], latest_counter)

        file = request.files['study_material']
        if file.filename == '':
            return {'message': 'The uploaded file has no filename'}
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_name_list = filename.split('.')
            file_path = os.path.normpath(os.path.join(self.UPLOAD_FOLDER_ASSIGNMENTS_PATH, material_code + '.' +
                                                      file_name_list[len(file_name_list)-1]))
            file.save(file_path)

        material_path = file_path

        material = MaterialUploadModel(data['teacher_code'], material_code, data['upload_date'], data['course'],
                                       data['discipline'], data['subject_code'], data['semester'],
                                       data['deadline_date'], data['material_type'], material_path)



        material.save_to_db()
        return {
            'message': 'material saved successfully!!!'
        }, 201





