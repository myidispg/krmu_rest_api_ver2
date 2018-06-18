import os

import werkzeug
from flask import send_file
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from werkzeug.utils import secure_filename

from models.discipline import Discipline
from models.material_submission import MaterialSubmissionModel
from models.material_upload import MaterialUploadModel
from models.student_main import StudentMain


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
    parser.add_argument('study_material', type=werkzeug.datastructures.FileStorage, required=False, location='files')

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'ppt', 'docx'])
    UPLOAD_FOLDER_ASSIGNMENTS_PATH = "C:\KRMU_App\database\study-material\material-upload"

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def generate_material_code(self, discipline, semester, subject_code, material_type, counter):
        code = discipline + "-" + semester + '-' + subject_code + '-' + material_type + '-' + counter
        return code

    def populate_submission_table(self, course, discipline, semester, material_code):
        roll_no_list = StudentMain.find_by_course_discipline_semester(course, discipline, semester)
        for roll_no in roll_no_list:
            material_submission = MaterialSubmissionModel(material_code, roll_no, None, None, None)
            material_submission.save_to_db()

    def post(self):
        data = MaterialUploadResource.parser.parse_args()

        discipline = Discipline.get_short_form(data['discipline'])
        latest_counter = MaterialUploadModel.get_material_counter(discipline + "-" + data['semester']
                                                                  + '-' + data['subject_code'] + '-' +
                                                                  data['material_type'])
        material_code = self.generate_material_code(discipline, data['semester'],
                                                    data['subject_code'], data['material_type'], latest_counter)

        if data['study_material'] is not None:
            file = data['study_material']
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

            self.populate_submission_table(data['course'], data['discipline'], data['semester'],
                                           material_code)
            material.save_to_db()
            return {
                       'message': 'material saved successfully!!!'
                   }, 201
        else:
            material_path = None
            material = MaterialUploadModel(data['teacher_code'], material_code, data['upload_date'], data['course'],
                                           data['discipline'], data['subject_code'], data['semester'],
                                           data['deadline_date'], data['material_type'], material_path)
            self.populate_submission_table(data['course'], data['discipline'], data['semester'],
                                           material_code)
            material.save_to_db()
            return {'message': 'material saved without file'}


class MaterialSubmissionResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('material_code', type=str, required=True, help='material_code is required')
    parser.add_argument('roll_no', type=str, required=True, help='roll_no is required')
    parser.add_argument('submission_date', type=str, required=True, help='submission_date is required')
    parser.add_argument('submission_file', type=werkzeug.datastructures.FileStorage, required=True,
                        help='submission_file is required', location='files')

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'ppt', 'docx'])
    UPLOAD_FOLDER_SUBMISSIONS_PATH = "C:\KRMU_App\database\study-material\student-submissions"

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def post(self):
        data = self.parser.parse_args()

        file = data['submission_file']
        if file.filename == '':
            return {'message': 'The uploaded file has no filename'}
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            material_code_split = data['material_code'].split('-')
            subject_code = material_code_split[2]
            counter = material_code_split[4]
            file_name_list = filename.split('.')
            file_path = os.path.normpath(os.path.join(self.UPLOAD_FOLDER_SUBMISSIONS_PATH, subject_code +
                                                      '-submission-' + counter + '-' + data['roll_no'] + '.' +
                                                      file_name_list[len(file_name_list)-1]))
            file.save(file_path)

            MaterialSubmissionModel.add_student_submission(data['submission_date'], file_path, data['material_code'],
                                                           data['roll_no'])

            return {'message': 'file submission successful'}


class StudentAssignmentMarksResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('material_code', type=str, required=True, help='material_code is required')
    parser.add_argument('student_roll_no', type=str, required=True, help='student_roll_no is required')
    parser.add_argument('marks_obtained', type=str, required=True, help='marks_obtained is required')

    def post(self):
        data = self.parser.parse_args()

        MaterialSubmissionModel.add_student_marks(data['material_code'], data['student_roll_no'], data['marks_obtained'])

        return {'message': 'Student submission marks updated successfully'}


class TeacherAllAssignmentResource(Resource):

    def get(self, teacher_code):
        study_material_all = {'study_material': []}

        material_list = MaterialUploadModel.get_all_by_teacher_code(teacher_code)
        for material in material_list:
            filename = material['material_path']
            file_list = filename.split('.')
            file_extension = file_list[1]
            material['material_path'] = file_extension
            study_material_all['study_material'].append(material)

        return study_material_all


class StudentAllAssignmentsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('roll_no', type=str, required=True, help='roll_no is required')

    def post(self):
        data = self.parser.parse_args()
        student = StudentMain.find_by_roll_number(data['roll_no'])

        discipline = student.discipline
        semester = student.current_sem

        material_list = MaterialUploadModel.get_all_by_discipline_semester(discipline, semester)

        return material_list


class StudentSingleAssignmentResource(Resource):  # Gets the details of a single assignment

    def get(self, material_code, roll_no):
        material = MaterialUploadModel.get_material_by_material_code(material_code)
        material['submission_date'] = MaterialSubmissionModel.get_submission_date_by_material_code(material_code,
                                                                                                   roll_no)

        return material


class TeacherSingleAssignmentResource(Resource):  # lets the teacher view a single assignment with submissions

    def get(self, material_code):
        material = MaterialUploadModel.get_material_by_material_code(material_code)
        submissions_list = MaterialSubmissionModel.get_all_by_material_code(material_code)
        material['submissions'] = submissions_list

        return material


class TeacherSingleAssignmentFileResource(Resource):  # Get the uploaded file by teacher

    def get(self, material_code):
        material_path = MaterialUploadModel.get_material_path_by_material_code(material_code)

        filename = material_path
        file_list = filename.split('.')
        file_extension = file_list[1]
        file_dictionary = {
            'filename': filename
        }
        # return send_file(file_dictionary['filename'], mimetype='text/' + file_extension)
        return send_file(file_dictionary['filename'])

